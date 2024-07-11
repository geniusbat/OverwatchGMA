import json
import os
import alert

#TODO: Iterate first through logs and then through rules (not rules -> logs)

class NginxRules():
    known_ips = [
        "127.0.0.1",#localhost
        "147.185.133.53", #Palo alto scanner
        "37.14.188.230",
        "95.127.33.6"
        ]
    access_logs = []
    rule_data_location = "nginx_rule_data"
    rule_data = {}
    alerts = []

    def __init__(self, input_access_logs):
        #Initialize stuff
        self.access_logs = input_access_logs
        self.alerts = []
        #Load data
        if os.path.exists(self.rule_data_location):
            with open(self.rule_data_location, 'r') as file:
                try:
                    self.rule_data = json.load(file)
                except:
                    self.alerts.append("Alert 16 - Could not load Nginx rule_data file at "+self.rule_data_location)
        else:
            self.rule_data = {}

    def try_rules(self):
        for log in self.access_logs:
            self.unusual_ips(log)
            self.high_amount_of_requests(log)
            self.unusual_http_petitions(log)

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
    
    #This will exclude known ips
    def high_amount_of_requests(self, log):
        threshold = 200
        if log["remote_address"] in self.rule_data["seenIps"].keys():
            if self.rule_data["seenIps"][log["remote_address"]] >= threshold:
                self.alerts.append("Alert 15 - High amount of request from unkown IP "+log["remote_address"]+" - "+json.dumps(log))
        else:
            self.rule_data["seenIps"][log["remote_address"]] = 1


    def unusual_http_petitions(self, log):
        if any(x in log["request_type"] for x in ["PUT", "DELETE", "TRACE", "PATCH"]):
            self.alerts.append("Alert 8 - Unusual http petition received - "+json.dumps(log))

    def reset_seen_ips_count(self):
        if "seenIps" in self.rule_data:
            for ip in self.rule_data["seenIps"].keys():
                self.rule_data["seenIps"][ip] = 1

    def write_output(self):
        #Sound alerts
        if len(self.alerts)>0:
            for indv_alert in self.alerts:
                alert.sound_alert(indv_alert)
        #Save rule_data
        data = json.dumps(self.rule_data)
        with open(self.rule_data_location, 'w') as file:
            file.write(data)