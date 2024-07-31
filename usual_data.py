#Store variables in this pseudo-environment that will be accessed but not changed much

import os

# ----------------------- GENERAL -----------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
DEBUG = True
PRINT_TO_TERMINAL = True

TELEGRAM_TOKEN_LOCATION = os.path.join(ROOT_DIR, "telegramCredentials")
TELEGRAM_CHAT_ID = "6953969784"


# ----------------------- NGINX -----------------------
BAN_FILE = os.path.join(ROOT_DIR, "ips_to_ban") #Make sure it is the same as in "list_ban.sh"

KNOWN_IPS = [
    "127.0.0.1",#localhost
    "147.185.133.53", #Palo alto scanner
    "37.14.188.230",
    "88.29.175.151",
    "52.46.83.62"
]

#Remember to update "project_url_locations" in nginxRules.py


# ----------------------- OS -----------------------
MONITOR_TEMP = False