import subprocess
import queue
import threading

#Add root path to import modules
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import exceptions


def run_command(command_path:str,user:str=None, parameters:list=[],q_output:queue.Queue=None,q_error:queue.Queue=None):
    #Set default user if None specified
    if user is None:
        user = 1000
    #Make sure command exists
    if os.path.exists(command_path):
        #Run subprocess
        process = subprocess.Popen([command_path]+parameters, stdout=subprocess.PIPE,stderr=subprocess.PIPE, user=user, text=True)
        #Get stdout and stderr
        stdout, stderr = process.communicate()
        #Kill process, most probably not needed by "just in case"
        process.kill()
        
        #Write process stdout to the output queue
        if q_output:
            result = {
                "command": os.path.split(command_path)[-1],
                "returncode": process.returncode, 
                "stdout": stdout.strip()
            }
            q_output.put(result)
        #Write process stderr if return code isn't 0 to error queue
        if q_error:
            if process.returncode > 0:
                error = {
                    "command": os.path.split(command_path)[-1],
                    "returncode": process.returncode, 
                    "stderr": stderr.strip()
                }
                q_error.put(error)
        
        return process.returncode, stdout
    #Command does not exist
    else:
        raise exceptions.CommandNotFound(command_path)