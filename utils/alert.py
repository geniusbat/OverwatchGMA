import sys
sys.path.append("..")

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import requests

import usual_data

def get_bot_token():
    try:
        with open(usual_data.TELEGRAM_TOKEN_LOCATION, mode="r", encoding="utf-8") as file:
            token = file.readline().strip(" ").strip("").strip("\n")
            return token
    except:
        print("Error extracting token")
        return None

def get_bot_updates():
    token = get_bot_token()
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    res = requests.get(url).json()
    print(res)
    return res

def sound_alert_debug(alert):
    print(alert)

def sound_alert(alert):
    if usual_data.DEBUG:
        sound_alert_debug(alert)
        return
    elif usual_data.PRINT_TO_TERMINAL:
        sound_alert_debug(alert)
    token = get_bot_token()
    message = alert.strip("\n")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={usual_data.TELEGRAM_CHAT_ID}&text={message}"

    res = requests.get(url).json()
    if res["ok"] in ["False", False]:
        print(res)
    #print(res)

if __name__ == '__main__':
    globals()[sys.argv[1]]() #To run any function do "python <function_name>"