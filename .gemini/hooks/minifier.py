#!/usr/bin/env python3
import sys
import json
import re
import os

# Add the hooks directory to the path so we can import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import utils
except ImportError:
    # Fallback if utils is not in the same directory or fails to import
    pass

def main():
    try:
        # Read the JSON payload from stdin
        input_data = sys.stdin.read()
        if not input_data:
            if 'utils' in globals():
                utils.send_hook_decision("allow")
            else:
                print(json.dumps({"decision": "allow"}))
            return
            
        data = json.loads(input_data)
        llm_request = data.get("llm_request", {})
        messages = llm_request.get("messages", [])
        
        # Regex to find tagged instruction blocks
        # DOTALL is crucial to match across newlines
        pattern = re.compile(r"<instruction>.*?</instruction>", re.DOTALL)
        
        # Pass 1: Count total instruction block occurrences across all turns
        total_matches = 0
        for msg in messages:
            if "content" in msg and isinstance(msg["content"], str):
                total_matches += len(pattern.findall(msg["content"]))
            elif "parts" in msg and isinstance(msg["parts"], list):
                for part in msg["parts"]:
                    if "text" in part and isinstance(part["text"], str):
                        total_matches += len(pattern.findall(part["text"]))

        # Fast exit: Nothing to minify
        if total_matches <= 1:
            if 'utils' in globals():
                utils.send_hook_decision("allow")
            else:
                print(json.dumps({"decision": "allow"}))
            return

        # Pass 2: Replace all but the VERY LAST instruction block with a placeholder
        replaced_count = 0
        def replacer(match):
            nonlocal replaced_count
            replaced_count += 1
            if replaced_count < total_matches:
                return "<instruction>[Previous instructions omitted for efficiency]</instruction>"
            return match.group(0)

        modified_messages = []
        for msg in messages:
            new_msg = msg.copy()
            if "content" in new_msg and isinstance(new_msg["content"], str):
                new_msg["content"] = pattern.sub(replacer, new_msg["content"])
            elif "parts" in new_msg and isinstance(new_msg["parts"], list):
                new_parts = []
                for part in new_msg["parts"]:
                    new_part = part.copy()
                    if "text" in new_part and isinstance(new_part["text"], str):
                        new_part["text"] = pattern.sub(replacer, new_part["text"])
                    new_parts.append(new_part)
                new_msg["parts"] = new_parts
            modified_messages.append(new_msg)

        # Send the modified messages back to the CLI
        output_payload = {
            "decision": "allow",
            "hookSpecificOutput": {
                "llm_request": {
                    "messages": modified_messages
                }
            }
        }
        print(json.dumps(output_payload))

    except Exception as e:
        # Failsafe: if something goes wrong, don't block the request, just allow it
        if 'utils' in globals():
            utils.send_hook_decision("allow")
        else:
            print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
