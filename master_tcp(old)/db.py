import sqlite3
import sys, os
from enum import Enum
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data

class COMMAND_TYPE(Enum):
    DELEGATE = 0
    DELEGATE_ERROR = 1
    MASTER = 2
    MASTER_ERROR = 3

def get_connection():
    connection = sqlite3.connect(usual_data.DB_DIR)
    return connection


#INITIALIZATION IS BEING MOVED TO DJANGO, THIS FILE JUST EXISTS FOR COMMAND_TYPE AND ANY OTHER HELPER FUNCTIONS TO INTERACT WITH THE DB OUTSIDE OF DJANGO


def initialize_table_delegate_controls(cursor):
    query = '''CREATE TABLE IF NOT EXISTS delegate_controls (
        id INTEGER PRIMARY KEY,
        host VARCHAR(16),
        timestamp INTEGER,
        command_name VARCHAR(25),
        returncode INTEGER,
        message TEXT
    );'''
    cursor.execute(query)

def initialize_table_delegate_errors(cursor):
    query = '''CREATE TABLE IF NOT EXISTS delegate_errors (
        id INTEGER PRIMARY KEY,
        host VARCHAR(16),
        timestamp INTEGER,
        command_name VARCHAR(25),
        returncode INTEGER,
        message TEXT
    );'''
    cursor.execute(query)

def initialize_table_master_controls(cursor):
    query = '''CREATE TABLE IF NOT EXISTS master_controls (
        id INTEGER PRIMARY KEY,
        host VARCHAR(16),
        timestamp INTEGER,
        command_name VARCHAR(25),
        returncode INTEGER,
        message TEXT
    );'''
    cursor.execute(query)

def initialize_table_master_errors(cursor):
    query = '''CREATE TABLE IF NOT EXISTS master_errors (
        id INTEGER PRIMARY KEY,
        host VARCHAR(16),
        timestamp INTEGER,
        command_name VARCHAR(25),
        returncode INTEGER,
        message TEXT
    );'''
    cursor.execute(query)

def initialize_table_hosts_registry(cursor):
    query = '''CREATE TABLE IF NOT EXISTS hosts_registry (
        id INTEGER PRIMARY KEY,
        host VARCHAR(16),
        ip VARCHAR(39),
        previous_ip VARCHAR(39),
        last_updated INTEGER,
        previous_last_updated INTEGER
    );'''
    cursor.execute(query)

def initialize_db(connection):
    cursor :sqlite3.Cursor = connection.cursor()
    initialize_table_delegate_controls(cursor)
    initialize_table_delegate_errors(cursor)
    initialize_table_master_controls(cursor)
    initialize_table_master_errors(cursor)
    connection.commit()
    return connection

if __name__ == "__main__":
    with get_connection() as conn:
        initialize_db(conn)
        print("Finished initializing database")