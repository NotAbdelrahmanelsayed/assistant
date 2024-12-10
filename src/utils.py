import rapidfuzz
from workspace import workspaces
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')#, filename="logger.txt")

def fallback_response(assistant, command):
    assistant.speak(f"Sorry, I couldn't confidently match your command: '{command}'. Could you try again or be more specific?")
    logging.info("Fallback response triggered for unclear command.")
    return "No valid action taken."

def register_command(trigger, handler):
    """
    Register a new voice command with its corresponding handler.
    :param trigger: The command phrase (e.g., "open workspace").
    :param handler: The function to execute when the command is triggered.
    """
    COMMANDS[trigger] = handler

def handle_open_workspace(assistant, command):
    workspace_name = command.replace("open workspace", "").strip()
    
    # Use fuzzy matching to find the best matching workspace
    best_match = None
    best_score = 0

    for name in workspaces:
        score = rapidfuzz.fuzz.ratio(workspace_name, name)
        if score > best_score:
            best_match = name
            best_score = score

    if best_score > 90:
        return assistant.handle_app_action(best_match, "open", workspace=True)
    elif best_score > 70:
        assistant.speak(f"Did you mean '{best_match}'? Please confirm.")
        return f"Low confidence match: {best_match}"
    else:
        assistant.speak("Sorry, I couldn't find a matching workspace.")
        return "No workspace matched."


def handle_open_app(assistant, command):
    return assistant.handle_app_action(command, "open")

def handle_close_app(assistant, command):
    return assistant.handle_app_action(command, "close")

def handle_exit(assistant, _):
    assistant.speak("Goodbye!")
    exit(0)

def handle_list_workspaces(assistant, _):
    workspace_names = ", ".join(workspaces.keys())
    response = f"Available workspaces are: {workspace_names}" if workspace_names else "No workspaces found."
    assistant.speak(response)
    return response

COMMANDS = {
    "open_workspace": {
        "patterns": ["open workspace", "launch workspace"],
        "handler": handle_open_workspace
    },
    "open_app": {
        "patterns": ["open", "start"],
        "handler": handle_open_app
    },
    "close_app": {
        "patterns": ["close", "shut down"],
        "handler": handle_close_app
    },
    "exit": {
        "patterns": ["exit", "quit", "stop"],
        "handler": handle_exit
    },
    "list_workspaces": {
        "patterns": ["list workspaces", "show workspaces"],
        "handler": handle_list_workspaces
    }
}
# Register commands
register_command("dev mode", handle_open_workspace)
register_command("open workspace", handle_open_workspace)
register_command("open", handle_open_app)
register_command("close", handle_close_app)
register_command("exit", handle_exit)
register_command("quit", handle_exit)
register_command("list work spaces", handle_list_workspaces)