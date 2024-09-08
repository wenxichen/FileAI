import os
import shutil
from pathlib import Path
import traceback

def move_files(original_folder, output_folder):
    """
    Move all files from the original folder to the output folder.

    This function moves all files (not directories) from the specified original folder
    to the specified output folder. If the output folder doesn't exist, it will be created.

    Args:
        original_folder (str): The path to the folder containing the files to be moved.
        output_folder (str): The path to the folder where the files will be moved.

    Raises:
        FileNotFoundError: If the original_folder does not exist.
        PermissionError: If there's no permission to access folders or move files.
        shutil.Error: If there's an error during the file moving process.
        Exception: For any other unexpected errors during the file moving process.

    Returns:
        None
    """
    try:
        # Ensure the original folder exists
        if not os.path.exists(original_folder):
            raise FileNotFoundError(f"The directory {original_folder} does not exist.")

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get a list of all items in the original folder
        items = os.listdir(original_folder)

        # Move each file (not directory) to the output folder
        for item in items:
            item_path = os.path.join(original_folder, item)
            if os.path.isfile(item_path):
                shutil.move(item_path, output_folder)
                print(f"Moved '{item}' to {output_folder}")

        print(f"All files have been moved from {original_folder} to {output_folder}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Permission denied: Unable to access folders or move files.")
    except shutil.Error as e:
        print(f"Error occurred while moving files: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        # Import start_directory from create_dummy.py
        from create_dummy import start_directory
    except ImportError as e:
        print("Error: Unable to import start_directory from create_dummy.py")
        print(f"Import Error: {e}")
        print("Traceback:")
        print(traceback.format_exc())
        print("Using default Desktop directory instead.")
        # Get the home directory of the current user
        home_directory = str(Path.home())
        start_directory = os.path.join(home_directory, 'Desktop')
    except SyntaxError as e:
        print("SyntaxError in create_dummy.py:")
        print(e)
        print("Traceback:")
        print(traceback.format_exc())
        print("Using default Desktop directory instead.")
        home_directory = str(Path.home())
        start_directory = os.path.join(home_directory, 'Desktop')
    except Exception as e:
        print(f"Unexpected error when importing from create_dummy.py: {e}")
        print("Traceback:")
        print(traceback.format_exc())
        print("Using default Desktop directory instead.")
        home_directory = str(Path.home())
        start_directory = os.path.join(home_directory, 'Desktop')

    print(f"User's start directory: {start_directory}")

    # Construct paths for original and output folders
    original_folder = os.path.join(start_directory, 'x')
    output_folder = os.path.join(start_directory, 'y')

    print(f"Moving files from {original_folder} to {output_folder}")
    move_files(original_folder, output_folder)