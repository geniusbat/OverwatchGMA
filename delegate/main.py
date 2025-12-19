

#Add root path to import modules
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data #Load usual_data

from utils import utils

from ssocket import SSocket

if __name__ == "__main__":
    config = utils.load_yaml("/home/phobos/Documents/Programing/OverwatchGMA/delegate/delegate_config.yml")
    print(config)