

#Add root path to import modules
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data
import threading
import queue

from utils import utils

from client import Client
from run_commands import run_command

if __name__ == "__main__":
    config = utils.load_yaml("/home/phobos/Documents/Programing/OverwatchGMA/delegate/delegate_config.yml")

    '''
    cl = Client("0.0.0.0", 8443, "/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", "/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
    cl.connect_send("Hola mundo")
    cl.close()
    '''
    tags :list[str] = config["tags"]
    ignore_tag_commands :list[str] = []
    if not config["ignore_tag_commands"] is None:
        ignore_tag_commands = config["ignore_tag_commands"]
    hostname :str = config["hostname"]
    commands_directory :str = config["commands_directory"]
    if not os.path.exists(commands_directory):
        raise FileNotFoundError("Commands directory not found at: {}".format(commands_directory))
    commands :dict[str:dict] = config["commands"]
    #Add tag commands while ignoring those set to be ignored by host
    for tag in tags:
        if tag in usual_data.tags: 
            tag_commands = usual_data.tags[tag]["commands"]
            for command_key in tag_commands.keys():
                if not command_key in ignore_tag_commands and not command_key in commands:
                    commands[command_key] = tag_commands[command_key]
    #print(commands)
    output_queue = queue.Queue()
    threads = []
    for command_key in commands.keys():
        command_info :dict = commands[command_key]
        #Skip command if disabled
        if "disabled" in command_info and command_info["disabled"]:
            continue
        #Check that command exists
        import datetime
        then = datetime.datetime.now()
        command_path = os.path.join(commands_directory, command_key)
        if os.path.exists(command_path):
            user = None
            parameters = []
            if "user" in command_info:
                user = command_info["user"]
            if "parameters" in command_info:
                parameters = command_info["parameters"]
            t = threading.Thread(target=run_command,kwargs={"command_path":command_path,"user":user,"parameters":parameters,"q":output_queue})
            threads.append(t)
            #status_code, message = run_command(command_path, user=user, parameters=parameters)
            #output += "{}[{}]:::{}".format(command_key,status_code,message)
        else:
            raise FileNotFoundError("Command not found at: {}".format(command_path))
    
    #Execute threads
    for t in threads:
        t.start()
    # Wait for all threads to finish
    for t in threads:
        t.join()
    result = ""
    while not output_queue.empty():
        command,status_code,message = output_queue.get()
        result += "{}[{}]:::{}".format(command,status_code,message)
    now = datetime.datetime.now()
    print(result)
    #print(run_command("/home/phobos/Documents/Programing/OverwatchGMA/commands/just_ls",user=1000,parameters=["/home"])[1])