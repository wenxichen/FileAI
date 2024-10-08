import os
import datetime
import time
import requests
import json

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
    

    
def find_with_llm(user_input, context):
    find_prompt = "Please find files based on the user's request: \"" + user_input + "\". Please only return a JSON object that has a key \"files\" and the value should be an array of files. Here's an example JSON response: {\"files\" : [{\"name\":\"dog_1.txt\", \"path\":\"'/Users/wchen/dog_1.txt\"}, {\"name\":\"dog_2.txt\", \"path\":\"/Users/wchen/dog_2.txt\"}]}. No explaination."
    prompt = f"{context}\n\n{find_prompt}"
    resp = make_llm_completion_call_return_json(prompt)
    try:
        resp = json.loads(resp)
    except json.JSONDecodeError:
        return 
    if "files" in resp:
        print("AI: ")
        for file in resp["files"]:
            print(file)
    else:
        return


def move_with_llm(user_input, context):
    find_where_to_move_to_prompt = "Please find the folder the user wants to move to based on the user's request: \"" + user_input + "\". Please only return a JSON object that has a key \"folder_path\" and the value should be the path to the folder. Here's an example JSON response: {\"folder_path\" : \"/Users/wchen/a/\"}. No explaination."
    prompt = f"{context}\n\n{find_where_to_move_to_prompt}"
    resp = make_llm_completion_call_return_json(prompt)
    try:
        resp = json.loads(resp)
    except json.JSONDecodeError:
        return 
    if "files" in resp:
        print("AI: ")
        for file in resp["files"]:
            print(file)
    else:
        return

def chat_with_llm(initial_context):
    print("\nStarting chat with LLM. Type 'exit' to end the conversation.")
    context = initial_context
 
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
 
        # user_input = f"{context}\n\nHuman: {user_input}\nAI:"
        action = check_user_request_action(user_input)
        
        if action == "find":
            print("Your action is to " + action + " files.")
            find_with_llm(user_input, context)
        elif action == "move":
            print("Your action is to " + action + " files.")
            pass
        else:
            print(f"\nAI: Sorry I am not able to help with this.")
        # if llm_response:
        #     response_content = llm_response.get('content', 'No content in response')
        #     print(f"\nAI: {response_content}")
        #     context += f"\nHuman: {user_input}\nAI: {response_content}"
        # else:
        #     print("\nFailed to get a response from the LLM.")
    print("Chat ended.")



def get_user_input():
        user_input = input("Enter your request: ")
        return user_input

if __name__ == "__main__":
    start_directory = os.getcwd()
 
    print(f"Scanning for files in {start_directory}")
 
     # Start the timer
    start_time = time.time()
 
    all_files, errors = get_all_files(start_directory)
 
    elapsed_time = time.time() - start_time
 
    print(f"Total files found: {len(all_files)}")
    print(f"Total files that could not be accessed: {errors}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
 
    # # Print the first 10 files as an example
    # print("First 10 files:")
    # for file in all_files[:10]:
    #     print(file)
 
    # Combine information of all files into a single string
    all_files_info = "\n".join([
        f"Name: {file['name']}, "
        f"Path: {file['path']}, "
        f"Size: {file['size']} bytes, "
        f"Modified: {file['modified']}"
        for file in all_files[:100]  # Limit to first 100 files to avoid token limit issues
    ])
 
    # Create initial context for the chat
    initial_context = f"""I have scanned {len(all_files)} files in {elapsed_time:.2f} seconds. 
Here are details of up to 100 files:
 
{all_files_info}
 
You are an AI assistant helping to analyze this file system information."""

    chat_with_llm(initial_context)

    # print("Your action is to " + check_user_request_action(user_input))

    #  # Start the timer
    # start_time = time.time()
    
    # all_files, errors = get_all_files(start_directory)
    
    # elapsed_time = time.time() - start_time
    
    # print(f"Total files found: {len(all_files)}")
    # print(f"Total files that could not be accessed: {errors}")
    # print(f"Time taken: {elapsed_time:.2f} seconds")
    
    # # Print the first 10 files as an example
    # # print("First 10 files:")
    # # for file in all_files[:10]:
    # #     print(file)

    # prompt = "You are a file manager. \nGiven the files information below \n\n\"\"\"\n" + str(all_files[:100]) + "\n\"\"\"\n\n" \
    #     + "Base on the file information above, what are files with \"cat\" in it's name?"

    # print(prompt)

    # print(make_llm_completion_call(prompt))

    # print(list_files())