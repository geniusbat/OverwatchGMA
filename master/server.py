# Simple HTTPS server in one file
import socket, ssl, json, datetime
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data

from utils import logger, exceptions

import db_commands, db

#CONFIGS
#Create unsecured socket
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) 
#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#Load certs. TODO: Do it dynamically
context.load_cert_chain(certfile="/home/zeus/Projects/Programacion/OverwatchGMA/master/certs/cert.pem", keyfile="/home/zeus/Projects/Programacion/OverwatchGMA/master/certs/key.pem")
context.set_ciphers("@SECLEVEL=1:ALL")
#Configure logger
#For testing do not write to disk
logger.log_path = ""
logger.FILE_HANDLER = False


def handle_results(data:dict):
    #Create connection to DB
    with db_commands.get_connection() as db_connection:
        logger.info("Received message from host {} at ip {}".format(data["hostname"],conn.getpeername()))
        #Store command result
        for command_name, command in data["results"].items():
            db_commands.store_command_message(
                db_connection,
                db.COMMAND_TYPE.DELEGATE,
                data["utcstamp"],
                data["hostname"],
                command_name,
                command["returncode"],
                command["stdout"],
            )

def handle_errors(data:dict):
    #Create connection to DB
    with db_commands.get_connection() as db_connection:
        logger.info("Received errors from host {} at ip {}".format(data["hostname"],conn.getpeername()))
        #Store command result
        for command_name, command in data["errors"].items():
            db_commands.store_command_message(
                db_connection,
                db.COMMAND_TYPE.DELEGATE_ERROR,
                data["utcstamp"],
                data["hostname"],
                command_name,
                command["returncode"],
                command["stderr"],
            )

#TODO: Define how to handle alerts
def handle_alert(data:dict):
    pass


#Start listening
logger.debug("TCP over SSL server running at https://0.0.0.0:{}".format(usual_data.COMS_PORT))
ssocket.bind(('0.0.0.0', usual_data.COMS_PORT))
ssocket.listen(5)
#Start handling connections
try:
    while True:
        conn, addr = ssocket.accept()
        #Secure socket in ssl
        conn = context.wrap_socket(conn, server_side=True)
        try:
            #Get whole message from buffer
            BUFFER_SIZE = 1024
            message = ""
            #Get the whole message (which has variable length)
            while True:
                part = conn.recv(BUFFER_SIZE)
                message += part.decode()
                # either 0 or end of data
                if len(part) < BUFFER_SIZE:
                    break
            #Message is assumed to be json, therefore convert it
            data = json.loads(message)

            #Check if key "type" is in data, if not log error and raise if required
            if not "type" in data:
                logger.error("Message from {} came without key 'type': {}".format(conn.getpeername(), data))
                if not exceptions.MessageWithoutType in usual_data.non_blocking_exceptions:
                    raise exceptions.MessageWithoutType("Message from {} came without key 'type': {}".format(conn.getpeername(), data))
            
            #Handle data if it is of type result
            if data["type"] == usual_data.DELEGATE_MESSAGE_TYPE.RESULTS.value:
                handle_results(data)
            #Handle data if it is of type error or the key "errors" is in data
            elif data["type"] == usual_data.DELEGATE_MESSAGE_TYPE.ERRORS.value or "errors" in data:
                handle_errors(data)
            elif data["type"] == usual_data.DELEGATE_MESSAGE_TYPE.ALERT.value:
                handle_alert(data) #TODO: Handle alerts
            else:
                logger.error("Request from {} couldn't be handled, it came with type {}".format(conn.getpeername(), data["type"]))
            
            #Store received hostname ip and check for incongruences
            with db.get_connection() as db_connection:
                #Check for incogruences
                incongruencias = db_commands.hosts_registry_check_if_ip_incongruent(db_connection,data["hostname"],conn.getpeername()[0])
                if len(incongruencias)>0:
                    for element in incongruencias:
                        message = "IP incongruences found for host {} with ip {}, which was registered as {} at {}".format(data["hostname"], conn.getpeername()[0], element[2],element[4])
                        logger.info(message)
                        db_commands.store_command_message(db_connection, db.COMMAND_TYPE.MASTER_ERROR, datetime.datetime.now(datetime.UTC).timestamp(), data["hostname"], "hosts_registry_check_if_ip_incongruent__db",0,message)
                #Register ip
                db_commands.hosts_registry_update(db_connection, data["hostname"], conn.getpeername()[0], data["utcstamp"])
        
        #Shutdown and disable receiving any more
        finally:
            conn.shutdown(socket.SHUT_RD)
#Close socket if receiving a KeyboardInterrupt 
except KeyboardInterrupt:
    ssocket.close()

logger.debug("Finished")