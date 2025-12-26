import os
import threading
#Add root path to import modules
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data

from .utils import load_yaml
from . import exceptions, logger

class CommandData():
    command_name : str
    command : str
    parameters : list[str]
    frequency : int
    user : int
    disabled : bool

    def __init__(self, command_name: str, command:str, parameters:list[str], frequency:int, user:int=1000, disabled:bool=False):
        self.command_name = command_name
        self.command = command
        self.parameters = parameters
        self.frequency = frequency #TODO: Maybe not needed here
        self.user = user
        self.disabled = disabled

        #Raise alarm of creating command that requires root without runing as root
        #TODO: Raise for other users (ie: command as user X and running as user Y)
        if user == 0 and not disabled:
            if os.getuid() != 0:
                raise exceptions.NotEnoughClearanceError("Command requires root but script isn't running as root:",self)

    def get_path(self,dir_path):
        return os.path.join(dir_path,self.command)


    def create_thread(self,run_func,commands_dir:str, output_queue=None, error_queue=None):
        command_path = os.path.join(commands_dir,self.command)
        if os.path.exists(command_path):
            t = threading.Thread(target=run_func,kwargs={"command_name":self.command_name,"command_path":command_path,"user":self.user,"parameters":self.parameters,"q_output":output_queue,"q_error":error_queue})
            return t
        else:
            raise exceptions.CommandNotFound(command_path)

    def __str__(self):
        dis = ""
        if self.disabled:
            dis = "(disabled)"
        return "{}{} as {} {}".format(self.command_name,dis,self.user,self.parameters)

class HostData():
    hostname : str
    log_file : str
    tags : list[str]
    commands_directory : str
    ignore_tag_commands : list[str]
    commands : dict[str:CommandData]
    cert_file : str
    key_file : str


    def load(self, host_path:str):
        if os.path.exists(host_path):
            config = load_yaml("/home/phobos/Documents/Programing/OverwatchGMA/delegate/delegate_config.yml")
            return self.init(config["hostname"],config.get("tags", []),config["commands_directory"],config["commands"],config["log_file"],config["cert_file"],config["key_file"],config.get("ignore_tag_commands", []))
        else:
            raise FileNotFoundError("Could not find config file at: {}".format(host_path))

    #Load and also handle tag commands
    def loadNhandle(self, host_path:str, tags_info:dict):
        self.load(host_path)
        self.handle_tag_commands(tags_info)
        return self

    #Load the class, it will not inherently handle commands inherited from tags, for that you need to use handle_tag_commands
    def init(self, hostname:str, tags:list[str], commands_directory:str, commands_raw:dict[str:dict],log_file:str, cert_file:str, key_file:str, ignore_tag_commands:list[str]=[]):
        self.hostname = hostname
        self.tags = tags
        self.commands_directory = commands_directory
        self.ignore_tag_commands = ignore_tag_commands
        self.log_file = log_file
        self.cert_file = cert_file
        self.key_file = key_file
        self.commands = {}
        if ignore_tag_commands is None:
            self.ignore_tag_commands = []
        raw_command : dict
        #Generate commands
        for key_raw, raw_command in commands_raw.items():
            try:
                parameters = raw_command.get("parameters",[])
                if not "frequency" in raw_command:
                    raise KeyError("frequency key could not be found in command: {} {}".format(key_raw,raw_command))
                frequency = raw_command["frequency"]
                real_command = raw_command["command"]
                user = raw_command.get("user",1000)
                disabled = raw_command.get("disabled",False)
                self.add_command(key_raw, real_command, parameters, frequency, user, disabled)
            except usual_data.non_blocking_exceptions as e:
                logger.warning("Exception thrown: {}".format(e))

        return self

    #Handle tag commands so all commands (from host and tags) are included to be used
    #This step is required when creating a HostData as __init__ doesn't "know" the tags information
    def handle_tag_commands(self,tags_info:dict):
        #Add tag commands that arent ignored
        for tag in tags_info:
            if tag in self.tags: 
                tag_commands = tags_info[tag]["commands"]
                for command_key in tag_commands.keys():
                    if not command_key in self.ignore_tag_commands and not command_key in self.commands:
                        try:
                            parameters = tag_commands[command_key].get("parameters",[])
                            if not "frequency" in tag_commands[command_key]:
                                raise KeyError("frequency key could not be found in command: {}".format(tag_commands[command_key]))
                            frequency = tag_commands[command_key]["frequency"]
                            real_command = tag_commands[command_key]["command"]
                            user = tag_commands[command_key].get("user",1000)
                            disabled = tag_commands[command_key].get("disabled",False)
                            self.add_command(command_key, real_command, parameters, frequency, user, disabled)
                        except usual_data.non_blocking_exceptions as e:
                            logger.warning("Exception thrown: {}".format(e))

    def add_command(self, command_name:str, command:str, parameters:list[str], frequency:int, user:int=1000, disabled:bool=False):
        #Do not add if already inside
        if not command_name in self.commands:
            try:
                c = CommandData(command_name, command, parameters, frequency, user, disabled)
                self.commands[command_name] = c
                return True
            except usual_data.non_blocking_exceptions as e:
                logger.warning("Exception thrown: {}".format(e))
            return False

    def append_command(self,command:CommandData):
        if not command.command_name in self.commands:
            self.commands[command_name] = c
            return True
        return False

    def __str__(self):
        command_str = ""
        for command_list in self.commands.values():
            for command in command_list:
                command_str += "{"+str(command)+"},"
        command_str = command_str[:-1]
        return "{} {}:{}".format(self.hostname,self.tags,command_str)