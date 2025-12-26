import yaml, os 

from . import exceptions


def load_yaml(file:str):
    if os.path.exists(file):
        with open(file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        raise FileExistsError("File not found at: {}".format(file))

#TODO: change bc i added the key "command" to the commands and "send_errors"
def validate_delegate_config_yaml(file:str):
    if os.path.exists(file):
        with open(file, "r") as yaml_file:
            data = yaml.safe_load(yaml_file)
            errors = ""
            if not "hostname" in data:
                errors += "Missing hostname\n"
            else:
                if data["hostname"] is None or data["hostname"] == "":
                    errors += "hostname is empty"
            if not "commands_directory" in data:
                errors += "Missing commands_directory\n"
            else:
                if data["commands_directory"] is None or data["commands_directory"] == "":
                    errors += "commands_directory is empty"
            if not "log_file" in data:
                errors += "Missing log_file\n"
            else:
                if data["log_file"] is None or data["log_file"] == "":
                    errors += "log_file is empty"
            if not "cert_file" in data:
                errors += "Missing cert_file\n"
            else:
                if data["cert_file"] is None or data["cert_file"] == "":
                    errors += "cert_file is empty"
            if not "key_file" in data:
                errors += "Missing key_file\n"
            else:
                if data["key_file"] is None or data["key_file"] == "":
                    errors += "key_file is empty"
            if "tags" in data:
                if data["tags"] is None:
                    errors += "tags is empty"
            if "ignore_tag_commands" in data:
                if data["ignore_tag_commands"] is None:
                    errors += "ignore_tag_commands is empty"
            if not "commands" in data:
                errors += "Missing commands\n"
            for command_key, command_data in data["commands"].items():
                if not "frequency" in command_data:
                    errors += "Missing frequency in command {}\n".format(command_key)
                if not "command_name" in command_data:
                    errors += "Missing command_name in command {}\n".format(command_key)
            if len(errors)>0:
                return "Errors in {}:\n{}".format(file,errors)
            else:
                return True
    else:
        raise FileExistsError("File not found at: {}".format(file))