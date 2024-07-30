import sys
sys.path.append("..")

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import rules.osRules as osRules
import utils.alert as alert

def test_os_rules():
    ins = osRules.OsRules()
    ins.try_rules()

def test_configuration():
    alert.sound_alert("This is a test from os rules, Am I working?")
    try:
        ins = osRules.OsRules()
    except:
        print("Something doesnt work in nginx rules")


if __name__ == "__main__":
    #To run any function do "python <function_name>"
    if len(sys.argv) >= 2:
        globals()[sys.argv[1]]()
    #Default process
    else:
        test_os_rules()