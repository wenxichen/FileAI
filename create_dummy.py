import os
from pathlib import Path

def create_folders_and_files(start_directory):
    """
    Create two folders ('x' and 'y') in the specified directory and populate 'x' with text files.

    This function creates a folder named 'x' and an empty folder named 'y' in the given directory.
    It then creates 10 text files named 'cat_01.txt' to 'cat_10.txt' inside the 'x' folder,
    each containing the text 'cat' followed by its filename.

    Args:
        start_directory (str): The directory where the folders and files will be created.

    Raises:
        FileNotFoundError: If the specified start_directory does not exist.
        PermissionError: If there's no permission to create folders in the start_directory.
        Exception: For any other unexpected errors during folder/file creation.

    Returns:
        None
    """
    try:
        # Ensure the start directory exists
        if not os.path.exists(start_directory):
            raise FileNotFoundError(f"The directory {start_directory} does not exist.")

        # Create a new folder named 'x' inside start_directory
        folder_x = os.path.join(start_directory, 'x')
        os.makedirs(folder_x, exist_ok=True)
        
        # Create 10 text files inside folder 'x'
        for i in range(1, 11):
            file_name = f"cat_{i:02d}.txt"
            file_path = os.path.join(folder_x, file_name)
            
            # Write content to each file
            with open(file_path, 'w') as file:
                file.write(f"cat {file_name}")
        
        # Create an empty folder named 'y' inside start_directory
        folder_y = os.path.join(start_directory, 'y')
        os.makedirs(folder_y, exist_ok=True)
        
        print(f"Created folder '{folder_x}' with 10 cat files in {start_directory}.")
        print(f"Created empty folder '{folder_y}' in {start_directory}.")
        print(f"Folders and files created successfully in {start_directory}")

    except PermissionError:
        print(f"Permission denied: Unable to create folders in {start_directory}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get the home directory of the current user
    # home_directory = str(Path.home())
    home_directory = os.getcwd()
    desktop_directory = os.path.join(home_directory, 'Desktop')
    print(f"User's Desktop directory: {desktop_directory}")
    
    start_directory = home_directory
    print(f"Creating folders and files in {start_directory}")
    create_folders_and_files(start_directory)
