import rapidfuzz
from AppOpener import give_appnames, open as open_app, close as close_app
from abc import ABC, abstractmethod

open_app("update", output=False) # Update Executables list.
THRESHOLD_SCORE = 70 

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class OpenCommand(Command):
    def __init__(self, app_name):
        self.app_name = app_name

    def execute(self):
        open_app(self.app_name, match_closest=True, output=False)


class CloseCommand(Command):
    def __init__(self, app_name):
        self.app_name = app_name

    def execute(self):
        close_app(self.app_name, match_closest=True, output=False)

class OpenApps:
    def __init__(self, command):
        self.command = command
        try:
            self.executables = give_appnames(upper=False)
        except Exception as e:
            raise RuntimeError(f"failed to retrieve app names: {e}")
        self.command_instance = None

    def match_executable(self):
        """
        Match the command against available executables using fuzzy matching.
        Returns (key, score).
        """
        return rapidfuzz.process.extractOne(
            self.command, self.executables, scorer=rapidfuzz.fuzz.partial_ratio
        )
    

    def set_command(self, action):
        """
        Set the command to open or close an application based on the action.
        """
        executable, _, _ = self.match_executable() or (None, 0)
        if not executable:
            return
        if action == "open":
            self.command_instance = OpenCommand(executable)
        elif action == "close":
            self.command_instance = CloseCommand(executable)

    def execute_command(self):
        """
        Execute the previously set command if confidence is above the threshold.
        """
        executable, score, _ = self.match_executable()
        if score >= THRESHOLD_SCORE and self.command_instance:
            self.command_instance.execute()
            return f"Executed action on {executable}."
        return f"Could not confidently match command. Found: {executable} (score: {score})."