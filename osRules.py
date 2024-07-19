import json
import os
import alert
import psutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class OsRules():
    rule_data_location = "" #Not used
    rule_data = {}
    alerts = []

    def __init__(self):
        #Initialize stuff
        self.alerts = []
        #Load data
        '''
        if os.path.exists(self.rule_data_location):
            with open(self.rule_data_location, 'r') as file:
                try:
                    self.rule_data = json.load(file)
                except:
                    self.alerts.append("Alert 16 - Could not load Nginx rule_data file at "+self.rule_data_location)
                    self.rule_data = {}
        else:
            self.rule_data = {}'''

    def try_rules(self):
        #Try rules
        self.near_full_disk_space()
        self.high_cpu_usage()
        self.high_ram_usage()

        #Write output
        self.write_output()

    def near_full_disk_space(self):
        threshold = 75 #Usage percentage that will alert of disk fullness
        highRiskThreshold = 90 
        hdd = psutil.disk_usage('/')
        if hdd.percent >= highRiskThreshold:
            self.alerts.append("Alert 16 - Disk space is at "+str(hdd.percent)+"% usage")
        elif hdd.percent >= threshold:
            self.alerts.append("Alert 8 - Disk space is at "+str(hdd.percent)+"% usage")
    
    def high_cpu_usage(self):
        threshold = 80
        highRiskThreshold = 98
        time = 5 #Interval, in seconds
        percent = psutil.cpu_percent(time)
        if percent > highRiskThreshold:
            self.alerts.append("Alert 16 - CPU space is at "+str(percent)+"% usage")
        elif percent >= threshold:
            self.alerts.append("Alert 8 - CPU space is at "+str(percent)+"% usage")

    def high_ram_usage(self):
        threshold = 75
        highRiskThreshold = 95
        percent = psutil.virtual_memory()[2]
        if percent > highRiskThreshold:
            self.alerts.append("Alert 16 - CPU space is at "+str(percent)+"% usage")
        elif percent >= threshold:
            self.alerts.append("Alert 8 - CPU space is at "+str(percent)+"% usage")


    def write_output(self):
        #Sound alerts
        if len(self.alerts)>0:
            for indv_alert in self.alerts:
                alert.sound_alert(indv_alert)
        else:
            alert.sound_alert("Alert 0 - OS Rules everythign alright")
        #Save rule_data
        '''
        data = json.dumps(self.rule_data)
        with open(self.rule_data_location, 'w') as file:
            file.write(data)'''