import os
import datetime
import time
import requests
import json
from pathlib import Path

# find all files and directories and their basic information in the current Windows directory
def list_files_in_current_directory():
    """Returns a list of all files and directories in the current Windows directory along with their basic information."""
    if not os.path.exists('.'):
        raise FileNotFoundError('The current directory does not exist.')
    if not os.path.isdir('.'):
        raise NotADirectoryError('The current path is not a directory.')
    try:
        file_list = []
        for file_or_dir in os.listdir():
            file_path = os.path.join('.', file_or_dir)
            file_list.append({
                'name': file_or_dir,
                'path': file_path,
                'is_file': os.path.isfile(file_path),
                'is_dir': os.path.isdir(file_path),
                'size': os.path.getsize(file_path),
                'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)),
                'created': datetime.datetime.fromtimestamp(os.path.getctime(file_path)),
                'accessed': datetime.datetime.fromtimestamp(os.path.getatime(file_path))
            })
        return file_list
    except PermissionError:
        raise PermissionError('Permission denied to access the current directory.')
    
import os

def get_all_files(start_path):
    file_list = []
    error_count = 0
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_info = {
                'name': file,
                'path': file_path,
                'is_file': os.path.isfile(file_path),
                'is_dir': os.path.isdir(file_path),
                'size': os.path.getsize(file_path),
                'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)),
                'created': datetime.datetime.fromtimestamp(os.path.getctime(file_path)),
                'accessed': datetime.datetime.fromtimestamp(os.path.getatime(file_path)) }
                file_list.append(file_info)
            except (OSError, PermissionError) as e:
                error_count += 1
                print(f"Error accessing file: {file_path}")
                print(f"Error message: {str(e)}")
    
    return file_list, error_count


def make_llm_completion_call(prompt):
    url = "http://192.168.3.7:8080/completion"
    response = requests.post(url, json={'prompt': prompt})
    response.raise_for_status()
    return response.json()['content']

def make_llm_completion_call_return_json(prompt):
    url = "http://192.168.3.7:8080/completion"
    response = requests.post(url, json={'prompt': prompt + "\n```json ", "stop": ["```"]})
    response.raise_for_status()
    return response.json()['content']


def check_user_request_action(input):
    prompt = f"""You are an AI assistant functioning as a file manager on a PC. Your task is to analyze the user's request and return a JSON object representing the action to be taken. Follow these steps:

    1. Determine the action: Is the user trying to find files or move files?
    2. Extract relevant information based on the action.
    3. Construct the JSON response according to the specified format.

    User request: "{input}"

    Response format:

    For "find" action:
    {{
        "action": "find",
        "input": {{
            "substring": "<search_term>"
        }}
    }}

    For "move" action:
    {{
        "action": "move",
        "input": [
            {{
                "original_folder": "<source_folder>",
                "output_folder": "<destination_folder>",
                "move_condition": "<condition_if_any>"
            }}
        ]
    }}

    For any other action:
    {{
        "action": "other"
    }}

    Rules:
    1. Always return a valid JSON object.
    2. Use "find" for searching or locating files.
    3. Use "move" for moving, copying, or transferring files.
    4. Use "other" if the action is neither find nor move.
    5. For "find", if no search term is found, use null for "substring".
    6. For "move", if any information is missing, use empty strings.
    7. Do not include any explanation or text outside the JSON object.

    Example responses:
    For "find my documents with 'report' in the name":
    {{"action": "find", "input": {{"substring": "report"}}}}

    For "move files from folder_a to folder_b":
    {{"action": "move", "input": [{{"original_folder": "folder_a", "output_folder": "folder_b", "move_condition": ""}}]}}

    Now, analyze the user's request and provide the appropriate JSON response:"""

    resp = make_llm_completion_call_return_json(prompt)
    if resp is None:
        print("Error: Unable to get a valid response from LLM after multiple attempts")
        return None

    print("Raw LLM response:", resp)
    
    try:
        resp_json = json.loads(resp)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from LLM")
        return None
    
    if "action" in resp_json and resp_json["action"] in ["find", "move", "other"]:
        global full_response
        full_response = resp_json
        return resp_json
    else:
        print("Error: Invalid action in LLM response")
        return None

def get_full_response():
    global full_response
    return full_response

if __name__ == "__main__":
    home_directory = str(Path.home())
    start_directory = os.path.join(home_directory, 'Desktop')
    
    print(f"Scanning for files in {start_directory}")

    user_input = input("Enter your request: ")

    action_data = check_user_request_action(user_input)
    if action_data is not None:
        action = action_data["action"]
        print(f"Your action is to {action}")
        if action == "find":
            search_term = action_data["input"]["substring"]
            print(f"Searching for files containing: {search_term}")
        elif action == "move":
            move_info = action_data["input"][0]
            print(f"Moving files from {move_info['original_folder']} to {move_info['output_folder']}")
            if move_info['move_condition']:
                print(f"Move condition: {move_info['move_condition']}")
        print("\nFull response:")
        print(json.dumps(action_data, indent=2))
    else:
        print("Unable to determine the action. Please try rephrasing your request.")