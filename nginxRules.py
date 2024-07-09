import json
import os
import alert

#TODO: Iterate first through logs and then through rules (not rules -> logs)

class NginxRules():
    known_ips = ["127.0.0.1"]
    access_logs = []
    rule_data_location = "nginx_rule_data"
    rule_data = {}
    alerts = []

    def __init__(self, input_access_logs):
        self.access_logs = input_access_logs
        self.alerts = []
        if os.path.exists(self.rule_data_location):
            with open(self.rule_data_location, 'r') as file:
                self.rule_data = json.load(file)
        else:
            self.rule_data = {}

    def try_rules(self):
        for log in self.access_logs:
            self.unusual_ips(log)
            self.high_amount_of_requests(log)

        #Write output
        self.write_output()

    def unusual_ips(self, log):
        #Initialize list
        if not "seenIps" in self.rule_data:
            self.rule_data["seenIps"] = {}
        
        #Check if ip is known
        #Ip not seen before
        if not log["remote_address"] in self.rule_data["seenIps"].keys() and not log["remote_address"] in self.known_ips:
            self.rule_data["seenIps"][log["remote_address"]] = 1
            self.alerts.append("Alert 8 - New IP "+log["remote_address"]+" - "+json.dumps(log))
        else:
            self.rule_data["seenIps"][log["remote_address"]] += 1
    
    #Run after unusual_ips. This will exclude known ips
    def high_amount_of_requests(self, log):
        threshold = 10

        if log["remote_address"] in self.rule_data["seenIps"].keys():
            if self.rule_data["seenIps"][log["remote_address"]] >= threshold:
                self.alerts.append("Alert 15 - High amount of request from unkown IP "+log["remote_address"]+" - "+json.dumps(log))

    def write_output(self):
        #Sound alerts
        if len(self.alerts)>0:
            for indv_alert in self.alerts:
                alert.sound_alert(indv_alert)
        
        #Save rule_data
        data = json.dumps(self.rule_data)
        with open(self.rule_data_location, 'w') as file:
            file.write(data)

NginxRules("").try_rules()