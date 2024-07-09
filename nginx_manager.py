#!/usr/bin/python

import utils
import alert
import os
import nginxRules

nginx_rules_location = "testAccesslog.txt"

def test_nginx_rules():
    if os.path.exists(nginx_rules_location):
        res = utils.parse_nginx_file(nginx_rules_location)
        nginxRules.NginxRules(res).try_rules()
        #with open(nginx_rules_location):
            #pass
            #utils.parse_nginx_file()
    else:
        alert.sound_alert("Nginx file does not exist")

if __name__ == "__main__":
    test_nginx_rules()