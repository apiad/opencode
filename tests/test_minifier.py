#!/usr/bin/env python3
import subprocess
import json
import sys
import os

def run_minifier(payload):
    process = subprocess.Popen(
        ['python3', '.gemini/hooks/minifier.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(payload))
    if stderr:
        print(f"Error: {stderr}")
    return json.loads(stdout)

def test_minifier():
    mock_payload = {
        "llm_request": {
            "messages": [
                {
                    "role": "system",
                    "content": "<instruction>Block 1: Expert Architect</instruction>"
                },
                {
                    "role": "user",
                    "content": "Hello"
                },
                {
                    "role": "model",
                    "content": "Hi there"
                },
                {
                    "role": "system",
                    "content": "<instruction>Block 2: Code Reviewer</instruction>"
                },
                {
                    "role": "user",
                    "content": "Check this code"
                },
                {
                    "role": "model",
                    "content": "Looks good"
                },
                {
                    "role": "system",
                    "content": "<instruction>Block 3: Expert Project Manager</instruction>"
                }
            ]
        }
    }

    print("Running minifier test...")
    result = run_minifier(mock_payload)
    
    messages = result["hookSpecificOutput"]["llm_request"]["messages"]
    
    # Assertions
    assert len(messages) == 7
    assert messages[0]["content"] == "<instruction>[Previous instructions omitted for efficiency]</instruction>"
    assert messages[3]["content"] == "<instruction>[Previous instructions omitted for efficiency]</instruction>"
    assert messages[6]["content"] == "<instruction>Block 3: Expert Project Manager</instruction>"
    
    # Check that model responses and user inputs are UNTOUCHED
    assert messages[1]["content"] == "Hello"
    assert messages[2]["content"] == "Hi there"
    assert messages[4]["content"] == "Check this code"
    assert messages[5]["content"] == "Looks good"

    print("✅ Minifier test passed! Successfully compressed 2/3 instruction blocks.")

if __name__ == "__main__":
    try:
        test_minifier()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
