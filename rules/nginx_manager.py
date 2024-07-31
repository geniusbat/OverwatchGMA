import sys
sys.path.append("..")

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import nginxRules
import utils.alert as alert
import utils.utils as utils
import usual_data
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

relative_nginx_logs_location = "testAccesslog.txt"

def test_nginx_rules():
    current_logs_location = get_logs_location(relative_nginx_logs_location)
    if os.path.exists(current_logs_location):
        res = utils.parse_nginx_file(current_logs_location)
        alerts = nginxRules.NginxRules(res).try_rules()
        #Sound alerts
        #TODO: IF too many aggregate alerts
        if len(alerts)>0:
            for indv_alert in alerts:
                alert.sound_alert(indv_alert)
        else:
            alert.sound_alert("Alert 0 - Nginx Rules everythign alright")
    else:
        alert.sound_alert("Nginx file does not exist")

def reset_seen_ips_count():
    ins = nginxRules.NginxRules([])
    ins.reset_seen_ips_count()
    ins.write_output()

def reset_banned_ips():
    ins = nginxRules.NginxRules([])
    ins.reset_banned_ips()
    ins.write_output()

def test_configuration():
    alert.sound_alert("This is a test, Am I working?")
    current_logs_location = get_logs_location(relative_nginx_logs_location)
    if os.path.exists(current_logs_location):
        res = utils.parse_nginx_file(current_logs_location)
        try:
            ins = nginxRules.NginxRules(res)
        except:
            print("Something doesnt work in nginx rules")
    else:
        alert.sound_alert("Nginx file does not exist")
    
def ban_current_ips():
    current_logs_location = get_logs_location(relative_nginx_logs_location)
    if os.path.exists(current_logs_location):
        res = utils.parse_nginx_file(current_logs_location)
        nginxRules.NginxRules(res).super_ban() #Add file location if custom needed
    else:
        alert.sound_alert("Nginx file does not exist")

def clean_logs():
    current_logs_location = get_logs_location(relative_nginx_logs_location)
    if os.path.exists(current_logs_location):
        open(current_logs_location, "w").close() #This will clear file
    else:
        alert.sound_alert("Nginx file does not exist")

def get_logs_location(relative_location):
    if usual_data.DEBUG:
        return os.path.join(usual_data.ROOT_DIR, "testingData", relative_location)
    else:#If not debug it is an absolute location
        return relative_location


if __name__ == "__main__":
    #To run any function do "python <function_name>"
    if len(sys.argv) >= 2:
        globals()[sys.argv[1]]()
    #Default process
    else:
        test_nginx_rules()