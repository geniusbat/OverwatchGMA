import requests
import sys

token_location = "telegramCredentials"
chat_id = "6953969784"

def get_bot_token():
    try:
        with open(token_location, mode="r", encoding="utf-8") as file:
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
    sound_alert_debug(alert)
    return
    token = get_bot_token()
    message = alert.strip("\n")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"

    res = requests.get(url).json()
    if res["ok"] in ["False", False]:
        print(res)
    #print(res)

if __name__ == '__main__':
    globals()[sys.argv[1]]() #To run any function do "python <function_name>"