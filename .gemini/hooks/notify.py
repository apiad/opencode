import subprocess
import os
import sys
from utils import send_hook_decision

def notify_user():
    """
    Sends a desktop notification using notify-send.
    Fails gracefully if notify-send is not available.
    """
    try:
        # Get the project root from git
        try:
            project_root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            project_name = os.path.basename(project_root)
        except Exception:
            # Fallback to current directory if not in a git repo
            project_name = os.path.basename(os.getcwd())
        
        # Determine the message based on the hook context
        message = f"Gemini CLI has finished in '{project_name}'"
        
        # Try to call notify-send
        subprocess.run(
            ["notify-send", "Gemini CLI", message, "--icon=terminal"],
            check=False,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
    except Exception:
        # Gracefully handle cases where notify-send is not installed or fails
        pass

if __name__ == "__main__":
    # Perform the notification
    notify_user()
    
    # Always allow the agent to proceed
    send_hook_decision("allow")
