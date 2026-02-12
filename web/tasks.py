import threading, schedule
import time, sys, os, django, datetime,icmplib
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
import requests

import main.models

#Add root path to import usual_data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data

#TODO: Debug if usual_data.DEBUG == TRUE

def _aux_now_timestamp():
    return datetime.datetime.now(datetime.UTC).timestamp()

def error_for_unregistered_delegate_controls():
    hosts = main.models.hosts_registry.objects.values_list('host', flat=True).distinct()
    controls = list(main.models.delegate_controls.objects.exclude(host__in=hosts).values_list('host', flat=True))
    errors = list(main.models.delegate_errors.objects.exclude(host__in=hosts).values_list('host', flat=True))
    controls = controls + errors
    unregistered_hosts = set(controls + errors)
    for host in unregistered_hosts:
        main.models.master_errors.objects.create(
            host = host,
            timestamp = _aux_now_timestamp(),
            command_name = "Unregistered controls",
            returncode = 1,
            message = f"Unregistered {controls.count(host)} controls for host {host}"
        )

def control_ping_hosts():
    hosts = main.models.hosts_registry.objects.all()
    for host in hosts:
        if host.check_ping:
            try:
                response = icmplib.ping(host.ip, count=2, interval=0.5, timeout=2.5)
                #If packet loss is lower than 1 means something was able to be sent (therefore a connection was made)
                if response.packet_loss < 1.0:
                    control = main.models.master_controls(
                        host = host.host,
                        timestamp = _aux_now_timestamp(),
                        command_name = f"host_registry ping",
                        returncode = 0,
                        message = f"Ping {host.host} with ip {host.ip}. Packet loss: {response.packet_loss}, avg_rtt: {response.avg_rtt}"
                    )
                    control.store()
                else:
                    main.models.master_errors.objects.create(
                        host = host.host,
                        timestamp = _aux_now_timestamp(),
                        command_name = f"host_registry ping",
                        returncode = 2,
                        message = f"Could not ping to {host.host} with ip {host.ip}"
                    )
            except icmplib.NameLookupError:
                main.models.master_errors.objects.create(
                    host = host.host,
                    timestamp = _aux_now_timestamp(),
                    command_name = f"host_registry ping",
                    returncode = 2,
                    message = f"Could not ping to {host.host} with ip {host.ip} - icmplib.NameLookupError"
                )

def error_havent_received_anything_for_host():
    warnStamp = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)).timestamp()
    for host in main.models.hosts_registry.objects.filter(last_time_seen__lt=warnStamp):
        main.models.delegate_errors.objects.create(
            host = host.host,
            timestamp = _aux_now_timestamp(),
            command_name = "No recent activity for host_registry",
            returncode = 2,
            message = f"No recent activity recorded in host_registry for host {host.host}, last seen {host.time}"
        )

if __name__ == "__main__":
    #Set tasks
    #Example: schedule.every(10).minutes.do(job)
    schedule.every().day.at("10:00").do(error_for_unregistered_delegate_controls)
    schedule.every(15).minutes.do(control_ping_hosts)
    schedule.every().day.at("00:14").do(control_ping_hosts)
    #Run scheduler
    print("Running schedule")
    #while False:
    while True:
        schedule.run_pending()
        time.sleep(1)