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

# def check_user_request_action(input):
#     prompt =  "You are a file manager on a PC.\nThe user request: \"" + \
#         input + "\nIs the user trying to find or move files? Please only return a JSON object that has a key \"action\" and a value being one of the three actions - \"move\", \"find\" and \"other\". Here's an example JSON response: {\"action\" : \"find\"}. No explaination."
#     resp = make_llm_completion_call_return_json(prompt)
#     print(resp)
#     # check if resp is valid json
#     try:
#         resp = json.loads(resp)
#     except json.JSONDecodeError:
#         return 
#     if "action" in resp and resp["action"] in ["find", "move", "other"]:
#         return resp["action"]
#     else:
#         return

def check_user_request_action(input):
    prompt = f"""You are a file manager on a PC.
    The user request: "{input}"

    Analyze the user's request and determine if they are trying to find or move files. 
    If the action is "find", look for a search term.
    If the action is "move", identify the original folder, output folder, and any move conditions.

    Return a JSON object with the following structure:

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
                "original_folder": "<original_folder>",
                "output_folder": "<output_folder>",
                "move_condition": "<move_condition>"
            }}
        ]
    }}

    For any other action:
    {{
        "action": "other"
    }}

    If no search term is found for "find" action, use null or an empty string for "substring".
    If any information is missing for "move" action, use empty strings for the missing fields.

    Please return only the JSON object without any additional explanation."""

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
        return resp_json["action"]
    else:
        print("Error: Invalid action in LLM response")
        return None

def get_full_response():
    global full_response
    return full_response

def get_user_input():
        user_input = input("Enter your request: ")
        return user_input

if __name__ == "__main__":
    home_directory = str(Path.home())
    start_directory = os.path.join(home_directory, 'Desktop')
    
    print(f"Scanning for files in {start_directory}")

    user_input = input("Enter your request: ")

    action = check_user_request_action(user_input)
    if action is not None:
        print(f"Your action is to {action}")
        full_resp = get_full_response()
        print("Full response:", json.dumps(full_resp, indent=2))
    else:
        print("Unable to determine the action. Please try rephrasing your request.")