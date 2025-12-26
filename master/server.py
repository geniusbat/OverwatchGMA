# Simple HTTPS server in one file
import socket, ssl, json
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data

from utils import logger

import db_commands, db

ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", keyfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
context.set_ciphers("@SECLEVEL=1:ALL")

#ssocket = context.wrap_socket(ssocket, server_side=True)

#Set logger to not write logs to file
logger.FILE_HANDLER = False

#print("TCP over SSL server running at https://0.0.0.0:{}".format(usual_data.COMS_PORT))
logger.debug("TCP over SSL server running at https://0.0.0.0:{}".format(usual_data.COMS_PORT))
ssocket.bind(('0.0.0.0', usual_data.COMS_PORT))
ssocket.listen(1)
#Go receive data
try:
    while True:
        conn, addr = ssocket.accept()
        conn = context.wrap_socket(conn, server_side=True)
        try:
            BUFFER_SIZE = 1024
            message = ""
            #Get the whole message (which has variable length)
            while True:
                part = conn.recv(BUFFER_SIZE)
                message += part.decode()
                # either 0 or end of data
                if len(part) < BUFFER_SIZE:
                    break
            data = json.loads(message)
            #Create connection to DB
            db_connection = db_commands.get_connection()
            db.initialize_db(db_connection)
            logger.info("Received message from host {} at ip {}".format(data["hostname"],conn.getpeername()))
            #Store hostname ip
            db_commands.hosts_registry_update(db_connection, data["hostname"], conn.getpeername()[0], data["utcstamp"])
            #Check ip incongruencies #TODO: Investigate if it is better to keep this checking outside using scheduling
            incongruencias = db_commands.hosts_registry_check_for_incongruent_ips(db_connection)
            for row in incongruencias:
                logger.warning("Host IP changed for {} from {} to {}".format(row[1],row[2],row[3]))
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
            #resp = "YES"
            #conn.send(resp.encode())
        finally:
            conn.shutdown(socket.SHUT_RD)
            #conn.close()
except KeyboardInterrupt:
    ssocket.close()

logger.debug("Finished")