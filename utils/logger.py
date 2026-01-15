import logging

#Add root path to import modules
import sys
import os
from . import utils, structs

FILE_HANDLER :bool = False #True if logs should be written to disk
LOG_LEVEL :int = logging.DEBUG #Minimum log level to log
log_path :str = None #Log path if written to disk
extra_handlers : list[logging.Handler] = []

#Writting logs to disk is done either by setting "log_path", passing a valid parameter "log_file" to the 

def set_log_path(path):
    if not path is None and not os.path.exists(path):
        error("Log file path does not exist: {}".format(path))
    log_path = path

def get_log_handler() -> logging.Logger:
    aux_handlers = [logging.StreamHandler()]
    #Get file to log only if needed
    if FILE_HANDLER:
        #log_path is defined
        if not log_path is None:
            aux_handlers.append(logging.FileHandler(log_path))
        #log_path not defined
        elif log_path is None:
            raise FileNotFoundError("Please either define a log_path if desiring to write logs to disk")

    if len(aux_handlers)>0:
        aux_handlers.extend(aux_handlers)

    #Set logging config
    logging.basicConfig(level=LOG_LEVEL,
        handlers=aux_handlers,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )
    return logging.getLogger()


def debug(message:str):
    logger = get_log_handler()
    logger.debug(message)

def info(message:str):
    logger = get_log_handler()
    logger.info(message)

def warning(message:str):
    logger = get_log_handler()
    logger.warning(message)

def error(message:str):
    logger = get_log_handler()
    logger.error(message)