#!/usr/bin/env -S /bin/sh -c '"$(dirname "$0")/../../.venv/bin/python3" "$0" "$@"'
#Previous line uses python venv that is in root of project

import sqlite3, sys

#Import the root of project
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(SCRIPT_DIR))) #I run dirname twice to go back 2 times. #TODO: Improve to not have to run dirname twice but instead join regressively
import usual_data #Load usual_data
from utils import logger

#TODO: Logs to db or website to be displayed

if __name__ == "__main__":
    #Configure logger
    logger.log_path=os.path.join("/var/log/overwatchgma/check_host_ip_incongruencies_errors.log")
    #Get incongruences
    with sqlite3.connect(usual_data.DB_DIR) as connection:
        cursor : sqlite3.Cursor = connection.cursor()
        query = "SELECT * FROM hosts_registry WHERE ip != previous_ip;"
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res)==0:
            logger.FILE_HANDLER = False
            logger.info("No incongruences found")
        else:
            logger.FILE_HANDLER = True
            logger.error("From script 'check_host_ip_incongruencies.py' incongruences found:\n{}".format(res))