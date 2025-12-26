import yaml, os

file = "/home/phobos/Documents/Programing/OverwatchGMA/delegate/phobos_delegate.log"
if os.path.exists(file):
    with open(file, "r") as yaml_file:
        print(yaml_file.readlines())
        print(yaml.safe_load(yaml_file))
else:
    raise FileExistsError("File not found at: {}".format(file))