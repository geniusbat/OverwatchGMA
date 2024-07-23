import os
import sys
import nginxRules
import utils
import alert

os.chdir(os.path.dirname(os.path.abspath(__file__)))

nginx_logs_location = "testAccesslog.txt"
ban_file = "ips_to_ban"

def test_nginx_rules():
    if os.path.exists(nginx_logs_location):
        res = utils.parse_nginx_file(nginx_logs_location)
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
    if os.path.exists(nginx_logs_location):
        res = utils.parse_nginx_file(nginx_logs_location)
        try:
            ins = nginxRules.NginxRules(res)
        except:
            print("Something doesnt work in nginx rules")
    else:
        alert.sound_alert("Nginx file does not exist")
    
def ban_current_ips():
    if os.path.exists(nginx_logs_location):
        res = utils.parse_nginx_file(nginx_logs_location)
        nginxRules.NginxRules(res).super_ban() #Add file location if custom needed
    else:
        alert.sound_alert("Nginx file does not exist")

def clean_logs():
    if os.path.exists(nginx_logs_location):
        open(nginx_logs_location, "w").close() #This will clear file
    else:
        alert.sound_alert("Nginx file does not exist")


if __name__ == "__main__":
    #To run any function do "python <function_name>"
    if len(sys.argv) >= 2:
        globals()[sys.argv[1]]()
    #Default process
    else:
        test_nginx_rules()