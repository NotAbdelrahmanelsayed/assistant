import rapidfuzz
from AppOpener import give_appnames, open as _open, close as _close
from abc import ABC, abstractmethod

_open("update", output=False) # Update Executables list.


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class OpenCommand(Command):
    def __init__(self, app_name):
        self.app_name = app_name

    def execute(self):
        _open(self.app_name, match_closest=True, output=False)


class CloseCommand(Command):
    def __init__(self, app_name):
        self.app_name = app_name

    def execute(self):
        _close(self.app_name, match_closest=True, output=False)

class OpenApps:
    def __init__(self, command):
        self.command = command
        self.executables = give_appnames(upper=False)
        self.command_instance = None

    def get_executable(self):
        key, score, _ = rapidfuzz.process.extractOne(
            self.command, self.executables, scorer=rapidfuzz.fuzz.partial_ratio
        )
        return key, score

    def set_command(self, action):
        executable = self.get_executable()[0]
        if action == "open" and executable:
            self.command_instance = OpenCommand(executable)
        elif action == "close" and executable:
            self.command_instance = CloseCommand(executable)

    def execute_command(self):
        key, score = self.get_executable()
        if score > 70:
            self.command_instance.execute()
            return f"opened {key}"
        return f"Just found key:{key} with score:{score}"