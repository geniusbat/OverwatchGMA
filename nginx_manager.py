#!/usr/bin/python

import os
import sys
import nginxRules
import utils
import alert

nginx_rules_location = "testAccesslog.txt"

def test_nginx_rules():
    if os.path.exists(nginx_rules_location):
        res = utils.parse_nginx_file(nginx_rules_location)
        nginxRules.NginxRules(res).try_rules()
    else:
        alert.sound_alert("Nginx file does not exist")

def reset_seen_ips_count():
    ins = nginxRules.NginxRules([])
    ins.reset_seen_ips_count()
    ins.write_output()

if __name__ == "__main__":
    #To run any function do "python <function_name>"
    if len(sys.argv) >= 2:
        globals()[sys.argv[1]]()
    #Default process
    else:
        test_nginx_rules()