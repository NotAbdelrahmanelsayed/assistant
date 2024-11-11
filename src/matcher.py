import rapidfuzz
from AppOpener import give_appnames, open as _open, close as _close

triggers = ["open", "launch", "start", "run", "execute"]
executables = give_appnames(upper=False)
command = "oben gogle chrom"

def is_open(command, triggers):
    """
    function to check if the query contains open 
    """
    key, score, index = rapidfuzz.process.extractOne(command, triggers, scorer=rapidfuzz.fuzz.partial_ratio)
    if score > 70:
        return True
    return False


def get_executable(command, executables):
    """
    function to cheeck if the query have an executable
    """
    key, score, index = rapidfuzz.process.extractOne(command, executables, scorer=rapidfuzz.fuzz.partial_ratio)
    if score > 70:
        return key
    print(f"just found key: {key} with score {score}")


def open_executable(command):
    """
    function to open the executable.
    """
    _open(command, match_closest=True, output=False)

def close_executable(command):
    _close(command, match_closest=True, output=False)


def main_matcher(command, triggers=triggers, executables=executables):
    # check command opens
    if is_open(command, triggers):
        key = get_executable(command, executables)
        _open(key)


def close_recent(command):
    
    pass