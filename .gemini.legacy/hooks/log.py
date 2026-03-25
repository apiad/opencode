#!/usr/bin/env python3
"""
Hook to log request and tool data throughout the agent lifecycle.
Provides a structured view of what is sent to the API and tool executions.
"""
import sys
import os
import json

# Add the hooks directory to path for importing utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils

def main():
    """
    Main entry point for the logging hook.
    """
    try:
        input_data = sys.stdin.read()
        if not input_data:
            utils.send_hook_decision("allow")
            return

        data = json.loads(input_data)
        hook_event = data.get("hook_event_name", "Unknown")

        # Structured markers as requested
        header = f"--- {hook_event.upper().replace('_', ' ')} ---"
        footer = "-" * len(header)

        log_entry = f"\n{header}\n"

        # We log the full JSON for transparency, but could filter based on event if needed
        # For now, keeping it verbose as per previous instruction "EXACTLY what is being sent"
        log_entry += json.dumps(data, indent=2, ensure_ascii=False)

        log_entry += f"\n{footer}\n"

        utils.log_message(log_entry, mode="a")
        utils.send_hook_decision("allow")

    except Exception as e:
        sys.stderr.write(f"Error in logging hook: {str(e)}\n")
        utils.send_hook_decision("allow")

if __name__ == "__main__":
    main()
