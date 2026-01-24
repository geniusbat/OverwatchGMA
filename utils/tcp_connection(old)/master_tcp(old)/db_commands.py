import sqlite3
import db

#Add root path to import modules
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data

from utils import logger
logger.FILE_HANDLER = False

def get_connection():
    connection = sqlite3.connect(usual_data.DB_DIR)
    return connection

def store_command_message(connection, status:db.COMMAND_TYPE, timestamp:int, host:str, command_name:str, returncode:int, message:str):
    if status == db.COMMAND_TYPE.DELEGATE:
        insert_query = '''
            INSERT INTO delegate_controls(host,timestamp,command_name,returncode,message) 
            VALUES(?,?,?,?,?);
        '''
    elif status == db.COMMAND_TYPE.MASTER: #TODO: Create active controls
        insert_query = '''
            INSERT INTO master_controls(host,timestamp,command_name,returncode,message) 
            VALUES(?,?,?,?,?);
        '''
    elif status == db.COMMAND_TYPE.DELEGATE_ERROR:
        insert_query = '''
            INSERT INTO delegate_errors(host,timestamp,command_name,returncode,message) 
            VALUES(?,?,?,?,?);
        '''
    elif status == db.COMMAND_TYPE.MASTER_ERROR:
        insert_query = '''
            INSERT INTO master_errors(host,timestamp,command_name,returncode,message) 
            VALUES(?,?,?,?,?);
        '''
    cursor : sqlite3.Cursor = connection.cursor()
    cursor.execute(insert_query, (
            host, timestamp, command_name, returncode, message
        )
    )
    connection.commit()

def hosts_registry_update(connection, host: str, ip:str, timestamp:int):
    query_check_exists = "SELECT id, ip, last_time_seen FROM hosts_registry WHERE host = ?;"
    cursor : sqlite3.Cursor = connection.cursor()
    cursor.execute(query_check_exists, [host])
    check_result = cursor.fetchall()
    #None returned, create row
    if len(check_result)==0:
        query_insert = """INSERT INTO hosts_registry
            (host, ip, previous_ip, last_time_seen, previous_last_time_seen)
            VALUES
            (?, ?, '', ?, '');
        """
        cursor.execute(query_insert, [host, ip, timestamp])
        connection.commit()
    #One row exists, update
    if len(check_result)==1:
        query_update = """UPDATE hosts_registry SET
        ip=?, previous_ip=?, last_time_seen=?, previous_last_time_seen=?
        WHERE id=?;
        """
        cursor.execute(query_update, [ip, check_result[0][1], timestamp, check_result[0][2],check_result[0][0]])
        connection.commit()
    #Warn if more than one returned
    else:
        logger.warning("More than one record for host {} in hosts_registry".format(host))

def hosts_registry_check_for_incongruent_ips(connection):
    cursor : sqlite3.Cursor = connection.cursor()
    query = "SELECT * FROM hosts_registry WHERE ip != previous_ip;"
    cursor.execute(query)
    return cursor.fetchall()

def hosts_registry_check_if_ip_incongruent(connection, hostname:str, ip:str):
    cursor : sqlite3.Cursor = connection.cursor()
    query = "SELECT * FROM hosts_registry WHERE host = ? AND ip != ?;"
    cursor.execute(query, [hostname,ip])
    return cursor.fetchall()


def get_table(connection, table_name:str, extra_filter: str=""):
    query = 'SELECT * FROM table_name;'
    query = query.replace("table_name",table_name)
    #Add extra_filter to query
    if len(extra_filter)>0:
        query = query[:-1]
        query += extra_filter
        if query[-1] != ";":
            query += ";"
    cursor : sqlite3.Cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def delegate_controls_get(connection, extra_filter: str=""):
    query = 'SELECT * FROM delegate_controls;'
    #Add extra_filter to query
    if len(extra_filter)>0:
        query = query[:-1]
        query += extra_filter
        if query[-1] != ";":
            query += ";"
    cursor : sqlite3.Cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()
    

