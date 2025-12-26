import sqlite3
import sys, os
from enum import Enum
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data

class COMMAND_TYPE(Enum):
    DELEGATE = 0
    MASTER = 1
    ERROR = 2

def get_connection():
    connection = sqlite3.connect(usual_data.DB_DIR)
    return connection

def initialize_table_passive_controls(cursor):
    query = '''CREATE TABLE IF NOT EXISTS passive_controls (
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
    initialize_table_passive_controls(cursor)
    initialize_table_hosts_registry(cursor)
    connection.commit()
    return connection
