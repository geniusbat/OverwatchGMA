from enum import Enum
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

from utils import exceptions

#All timestamps should be as utc time, conversion will be done in the frontend

DEBUG = True

MASTER_IP = "127.0.0.1"
API_PORT = "8000"
API_HTTPS = False

DB_DIR = "./db.db"

tags = {
    "ubuntu": {
        "commands": {
            "high_cpu_usage": {
                "command": "cpu_usage",
                "frequency": 5
            },
            "root_filesystem_usage": {
                "command": "filesystem_usage",
                "parameters": ["/"],
                "frequency": 45
            },
        }
    },

}



non_blocking_exceptions = (
    exceptions.NotEnoughClearanceError,
    ConnectionResetError,
    exceptions.MessageWithoutType
)

class DELEGATE_MESSAGE_TYPE(Enum):
    RESULTS = 0
    ERRORS = 1
    ALERT = 2

COMS_PORT = 6707 #Unused, as it was used for tcp connection