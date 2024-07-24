import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class NginxRules():
    known_ips = [
        "127.0.0.1",#localhost
        "147.185.133.53", #Palo alto scanner
        "37.14.188.230",
        "88.29.175.151",
        "52.46.83.62"
        ]
    #TODO: This solution sucks
    project_url_locations = ["."] #Add django project locations that will be searched for urls.py to extract url names to make sure that even if the referrer is correct there isn't a weird url
    permitted_urls = []

    access_logs = []
    rule_data_location = "nginx_rule_data"
    rule_data = {}
    alerts = []
    ban_threshold = 6
    ban_file_location = ""
    outputed_ip = []

    #Remember to update weird_referrer() if u add new apps

    def __init__(self, input_access_logs, ban_threshold=6, ban_file_location="ips_to_ban"):
        #Initialize stuff
        self.access_logs = input_access_logs
        self.alerts = []
        self.ban_threshold = ban_threshold
        self.ban_file_location = ban_file_location
        #Get permitted urls
        self.update_permitted_urls()
        #Load data
        if os.path.exists(self.rule_data_location):
            with open(self.rule_data_location, 'r') as file:
                try:
                    self.rule_data = json.load(file)
                except:
                    self.alerts.append("Alert 16 - Could not load Nginx rule_data file at "+self.rule_data_location)
                    self.rule_data = {}
        else:
            self.rule_data = {}
    
    def weird_action(self, log):
        unusual_request = any(x in log["request_type"] for x in ["PUT", "DELETE", "TRACE", "PATCH"])
        return unusual_request
    
    def unknown_url(self, log):
        unknown_url = True
        for url in self.permitted_urls:
            if url in log["referer"]:
                unknown_url = False
                break
        return unknown_url

    def weird_referrer(self, log):
        from_unknown_app = not ("MoneyGMA" in log["referer"] or "moneygma" in log["referer"] or "tattoo" in log["referer"] or "Tattoo" in log["referer"])
        unknown_url = self.unknown_url(log)
        return from_unknown_app or unknown_url

    def try_rules(self):
        for log in self.access_logs:
            if log != None:
                self.unusual_successfull_actions(log)
                self.high_amount_of_requests(log)

        #Write output
        self.write_output()

        return self.alerts
    
    #This will exclude known ips
    def high_amount_of_requests(self, log):
        #Initialize seen ips
        if not "seenIps" in self.rule_data:
            self.rule_data["seenIps"] = {}
        
        #Try rule
        banable = False
        weird = False
        
        #It is something weird 
        if self.weird_action(log):
            weird = True
            banable = True

        #Get request status as int
        try:
            request_status = int(log["request_status"])
        except:
            request_status = 400
        #Weird referrer and status is failure
        if self.weird_referrer(log) and (400 <= request_status and request_status <= 499):
            weird = True

        #Log was weird therefore check if too many from that address
        if weird:
            #Address in dict
            if log["remote_address"] in self.rule_data["seenIps"].keys():
                self.rule_data["seenIps"][log["remote_address"]] += 1
            #Address not in dict
            else:
                self.rule_data["seenIps"][log["remote_address"]] = 1
            #Try to ban if already too many requests 
            if self.rule_data["seenIps"][log["remote_address"]] >= self.ban_threshold*2:
                banable = True
            #Alert if above threshold 
            if self.rule_data["seenIps"][log["remote_address"]] >= self.ban_threshold and not log["remote_address"] in self.outputed_ip:
                self.alerts.append("Alert 15 - High amount of request from unkown IP "+log["remote_address"]+" at "+str(self.rule_data["seenIps"][log["remote_address"]])+" requests - "+json.dumps(log))
                self.outputed_ip.append(log["remote_address"])
                #Also ban ip if necessary
                previously_banned_ips = self.rule_data.get("banned_ips",[])
                if banable and not log["remote_address"] in previously_banned_ips:
                    previously_banned_ips.append(log["remote_address"])
                    self.rule_data["banned_ips"]=previously_banned_ips
                    self.add_to_ban_file(log["remote_address"])
                    self.alerts.append("Alert 0 - Therefore the IP "+log["remote_address"]+" was banned.")


    def unusual_successfull_actions(self, log):
        #Get request status as int
        try:
            request_status = int(log["request_status"])
        except:
            request_status = 400
        
        if 200 <= request_status and request_status <= 399 and self.weird_referrer(log):
            self.alerts.append("Alert 13 - Successfull unexpected request from unkown IP "+log["remote_address"]+" - "+json.dumps(log))

    def reset_banned_ips(self):
        if "banned_ips" in self.rule_data:
            self.rule_data["banned_ips"] = []
        
    def reset_seen_ips_count(self):
        self.rule_data["seenIps"] = {}
    
    def super_ban(self, file_location="ips_to_ban"):
        threshold = 2
        count = {}
        to_ban = []
        for log in self.access_logs:
            #Not a known ip
            if log!=None and not log["remote_address"] in self.known_ips:
                #Weird action
                if self.weird_action(log):
                    if not log["remote_address"] in to_ban:
                        if log["remote_address"] in count:
                            count[log["remote_address"]] += 1
                        else:
                            count[log["remote_address"]] = 1
                        if count[log["remote_address"]]>=threshold:
                            to_ban.append(log["remote_address"])
        cad = ""
        for ip in to_ban:
            cad+=ip+"\n"
        with open(file_location, "w") as file:
            file.write(cad)

    def add_to_ban_file(self, ip):
        with open(self.ban_file_location, "a") as file:
            file.write(ip+"\n")

    def update_permitted_urls(self):
        self.permitted_urls = []
        for project_location in self.project_url_locations:
            for path, folders, files in os.walk(project_location):
                # Iterate over directories
                for folder in folders:
                    #Check if urls.py is inside, if so extract urls
                    if "urls.py" in os.listdir(f"{path}/{folder}"):
                        with open(os.path.join(project_location, folder, "urls.py"), "r") as file:
                            text = file.read().strip().replace("\n","")
                            res = re.findall(r"path\([\'\"].*?[\'\"],", text)
                            if res:
                                for result in res:
                                    url_result = re.search(r"[\'\"].*?[\'\"]", result)
                                    if url_result:
                                        url = url_result.group().replace("'","").replace("/","").replace("\"","")
                                        if not url in [" ", "", "\n", "admin"]:
                                            self.permitted_urls.append(url)


    def write_output(self):
        #Save rule_data
        data = json.dumps(self.rule_data)
        with open(self.rule_data_location, 'w') as file:
            file.write(data)