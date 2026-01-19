import time, traceback, queue, datetime, json, argparse
from typing import Tuple
#Add root path to import modules
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data 


from utils import utils, exceptions, logger
from utils.structs import HostData, CommandData
from client import Client
from run_commands import run_command



def handle_specific_commands(host:HostData, commands_queued:list[str]) -> Tuple[dict, dict]:
    #Create queues
    output_queue = queue.Queue()
    error_queue = queue.Queue()
    threads = []

    command : CommandData
    #Create commands in separate threads
    for command_key in commands_queued:
        command = host.commands[command_key]
        if not command.disabled:
            command_path = command.get_path(host.commands_directory)
            #Check if command exists
            if os.path.exists(command_path):
                try: 
                    #Create thread
                    t = command.create_thread(run_command,host.commands_directory,output_queue,error_queue)
                    threads.append(t)
                #Non-blocking exception raised, log and continue with following commands 
                except usual_data.non_blocking_exceptions as e:
                    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                    logger.warning("Exception thrown for {}: {}\n".format(command_key,e, traceback_str))
            #Command not found
            else:
                #CommandNotFound exception is set as non-blocking
                if exceptions.CommandNotFound in usual_data.non_blocking_exceptions:
                    logger.warning("{}[{}]:::{}".format(command_key,"ERROR","Command not found at: {}".format(command_path)))
                    error_queue.put({
                        "command_name": command_key,
                        "returncode": 127, 
                        "message": "Command not found at: {}".format(command_path)
                    })
                #CommandNotFound exception is set as blocking
                else:
                    raise exceptions.CommandNotFound(command_path) 
    
    #Execute threads
    for t in threads:
        t.start()
    # Wait for all threads to finish
    for t in threads:
        t.join()
    #Get results
    result = []
    while not output_queue.empty():
        output = output_queue.get()
        result.append(output)
    #Get thread errors
    errors = []
    #Log errors
    while not error_queue.empty():
        single_error = error_queue.get()
        logger.warning(single_error)
        errors.append(single_error)

    return result, errors

if __name__ == "__main__":
    #Define parameters
    parser=argparse.ArgumentParser()
    parser.add_argument("-c", help="Defines path of delegate config to use")
    args=parser.parse_args()
    try:
        #Get delegate_config file path from arguments
        config_dir = ""
        if args.c!=None and len(args.c)>0:
            config_dir = args.c
            #Make sure that file specified exits
            if not os.path.exists(config_dir):
                sys.exit("Configuration file {} does not exist".format(config_dir))
        else:
            sys.exit("No configuration file defined")

        #Load host data with tag commands
        host = HostData().loadNhandle(config_dir, usual_data.tags)
        #Configure logger
        if len(host.log_file) > 0:
           logger.FILE_HANDLER = True
           logger.log_path = host.log_file

        logger.debug("Correctly loaded config, starting delegate service with config {}".format(config_dir))

        #Get biggest frequency of all enabled commands
        biggest_frequency = 1
        for command_key,command_value  in host.commands.items():
            if command_value.frequency > biggest_frequency and not command_value.disabled:
                biggest_frequency = command_value.frequency
        
        #Main loop, timed at 1 minutes to run all required commands and send results to master 
        time_counter :int = 0
        while True:
            #Get commands to be executed
            commands_queued = []
            for command_key,command_value  in host.commands.items():
                if not command_value.disabled and time_counter % command_value.frequency == 0:
                    commands_queued.append(command_key)
            #Get current time
            utc_timestamp = int(datetime.datetime.now(datetime.UTC).timestamp())
            logger.debug("At time {} running commands: {}".format(time_counter, commands_queued))
            #Get result and errors
            result, errors = handle_specific_commands(host, commands_queued)
            #Log errors
            for error in errors:
                logger.error("Error when executing thread. Message: {}\n".format(error))
            #Add host and timestamp to results and errors to be sent to api
            result = [{**element,"host":host.hostname, 'timestamp': utc_timestamp} for element in result]
            errors = [{**element,"host":host.hostname, 'timestamp': utc_timestamp} for element in errors]
            #Connect to master and send packet
            try:
                #Create client to api
                cl = Client(usual_data.MASTER_IP,host.api_token,usual_data.API_PORT,usual_data.API_HTTPS) #TODO: Remove token before committing
                #Send controls
                if len(result)>0:
                    response = cl.post_delegate_controls(json.dumps(result))
                    #Something went wrong
                    if response.status_code > 300:
                        logger.warning("Something went wrong when sending controls to master: status code {}, message:\n{}".format(response.status_code,response.text))
                    #Everything alright
                    else:
                        logger.debug("Connection to master correct and sent data")
                #Send errors (if needed)
                if host.send_errors:
                    if len(errors)>0:
                        response = cl.post_delegate_errors(json.dumps(errors))
                    #Something went wrong
                    if response.status_code > 300:
                        logger.warning("Something went wrong when errors to master: status code {}, message:\n{}".format(response.status_code,response.text))
                    #Everything alright
                    else:
                        logger.debug("Sent errors to master correctly")
            #Handle connection refused
            except ConnectionRefusedError as e:
                traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                logger.error("Connection refused when sending to master:\n{}".format(traceback_str))
            
            #Finishing loop
            time_counter += 1
            #Reset time_counter if surpassing biggest frequency
            if time_counter>=biggest_frequency:
                time_counter = 0
            #Sleep for less if in debug
            if usual_data.DEBUG:
                time.sleep(2.5)
            else:
                time.sleep(60)
    #Catch all exceptions and log them
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        logger.error("{}\n{}".format(e,traceback_str))
        sys.exit(1)