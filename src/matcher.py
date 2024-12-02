import subprocess
import rapidfuzz
from AppOpener import give_appnames, open as open_app, close as close_app
from abc import ABC, abstractmethod
from workspace import workspaces
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

open_app("update", output=False) # Update Executables list.
THRESHOLD_SCORE = 70 

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class OpenCommand(Command):
    def __init__(self, app_name, workspace=False):
        self.app_name = app_name
        self.workspace = workspace

    def execute(self):
        if self.workspace:
            # Open a workspace using subprocess to call VS Code
            logging.info(f"Opening workspace: {self.app_name}")
            subprocess.call(["code", workspaces[self.app_name]], shell=True)
        else:
            # Open a regular app
            logging.info(f"Opening app: {self.app_name}")
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
            self.workspaces = workspaces
        except Exception as e:
            raise RuntimeError(f"failed to retrieve app names: {e}")
        self.command_instance = None

    def match_workspaces(self):
        """
        Match the command against available workspaces using fuzzy matching.
        Returns (key, score).
        """
        return rapidfuzz.process.extractOne(
            self.command, self.workspaces.keys(), scorer=rapidfuzz.fuzz.partial_ratio
        )
    
    def match_executable(self):
        """
        Match the command against available executables using fuzzy matching.
        Returns (key, score).
        """
        return rapidfuzz.process.extractOne(
            self.command, self.executables, scorer=rapidfuzz.fuzz.partial_ratio
        )
    

    def set_command(self, action, workspace=False):
        """
        Set the command to open or close an application or workspace based on the action.
        """
        if workspace:
            # Match against workspaces
            executable, score, _ = self.match_workspaces() or (None, 0)
            if executable and score >= THRESHOLD_SCORE:
                self.command_instance = OpenCommand(executable, workspace=True)
        else:
            # Match against executables (apps)
            executable, score, _ = self.match_executable() or (None, 0)
            if executable and score >= THRESHOLD_SCORE:
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