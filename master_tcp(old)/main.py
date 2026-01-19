

#Add root path to import modules
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data

import sqlite3, db

import db_commands

from utils import utils

if __name__ == "__main__":
    connection = sqlite3.connect("./db.db")#usual_data.DB_DIR)
    db.initialize_db(connection)
    import datetime
    #db_commands.store_command_message(connection, db.COMMAND_TYPE.DELEGATE, datetime.datetime.now(datetime.UTC), "test_host", "test_command", 0, "Hola Mundo")
    print(db_commands.get_table(connection, "hosts_registry"))