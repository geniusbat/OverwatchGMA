
class CommandNotFound(FileNotFoundError):
    def __init__(self, command_path:str):
        super().__init__("Command not found at: {}".format(command_path))

class ThreadExecutionError(ChildProcessError):
    pass

class NotEnoughClearanceError(PermissionError):
    pass

class DelegateConfigInvalidError(UserWarning):
    pass

class MessageWithoutType(UserWarning):
    pass