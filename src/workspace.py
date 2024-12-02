from urllib.parse import urlparse, unquote
import sqlite3
import json
import os
import platform

# Path to VS Code's state database
path = os.path.expandvars(r'%APPDATA%\Code\User\globalStorage\state.vscdb')

workspaces = {}

# Function to convert a file URI to a file path
def file_uri_to_path(file_uri):
    parsed = urlparse(file_uri)
    path = unquote(parsed.netloc + parsed.path)
    if platform.system() == "Windows":
        return path.replace('/', '\\')[1:] 
    return path 

try:
    # Open the SQLite database
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        # Query the recently opened pathes
        cursor.execute("SELECT value FROM ItemTable WHERE key LIKE 'history.recentlyOpenedPathsList';")
        result = cursor.fetchone()

        # Process the results if tit exists
        if result:
            recent_workspaces = json.loads(result[0])
            for entry in recent_workspaces['entries']:
                entry = entry.get('folderUri') or entry.get('workspace', {}).get('configPath')
                if entry:
                    entry = file_uri_to_path(entry)
                    name = entry.split("\\")[-1]
                    workspaces[name] = entry
except Exception as e:
    print(f"Error accessing the vs environments database: {e}")
if __name__ == "__main__":
    import pprint
    pprint.pprint(workspaces)


