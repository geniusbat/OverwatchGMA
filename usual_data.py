from enum import Enum
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

from utils import exceptions

#All timestamps should be as utc time, conversion will be done in the frontend

DEBUG = True

MASTER_IP = "127.0.0.1"
COMS_PORT = 6707

DB_DIR = "./db.db"

tags = {
    "ubuntu": {
        "commands": {
            "uname": {
                "command": "uname",
                "frequency": 1
            },
            
        }
    },

}



non_blocking_exceptions = (
    exceptions.NotEnoughClearanceError,
    ConnectionResetError
)

class DELEGATE_MESSAGE_TYPE(Enum):
    RESULTS = 0
    ERRORS = 1
    ALERT = 2