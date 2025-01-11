import subprocess
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Replace these with your Supabase project URL and API key
load_dotenv("env_file.txt") # Use a file different than .env since having a file called .env did not work on my phone
SUPABASE_URL = "https://ppfzupfcibjzuvxotlpm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBwZnp1cGZjaWJqenV2eG90bHBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0NjE1NTYsImV4cCI6MjA1MjAzNzU1Nn0.CdyUL3OXcVPUcjn6pDTtbG6vEIVr1RWyolHCQzElneI"

# Local path where the file will be temporarily stored
APP_PACKAGE_NAME = "com.unofficial.balatro"
REMOTE_FILE_PATH = "files/save/game/1/meta.jkr"
REMOTE_TMP_PATH = "/data/local/tmp/meta.jkr"
LOCAL_TMP_PATH = "meta.jkr"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pull_file_with_adb():
    """Uses adb to extract the file from the Android device."""
    # Run the adb command to copy the file to a temporary location
    adb_command = (
        f"adb shell \"mkdir -p /sdcard/Download && run-as {APP_PACKAGE_NAME} cat /data/data/{APP_PACKAGE_NAME}/files/save/game/1/meta.jkr > {REMOTE_TMP_PATH}\""
    )
    print(f"Executing: {adb_command}")
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Successfully pulled the file from the device.")
    else:
        print(f"Failed to pull the file from the device. Error: {result.stderr}")
    
def update_file_from_bucket(bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        return supabase.storage.from_(bucket_name).update(file=file, path=destination_path)   

def update_local_save_file():
    """Updates the local save file with the new data."""
    # Run the adb command to copy the file to the device
    adb_command = (
        f"adb shell \"run-as {APP_PACKAGE_NAME} cp -r {REMOTE_TMP_PATH} /data/data/{APP_PACKAGE_NAME}/files/save/game/1/meta.jkr\""
    )
    print(f"Executing: {adb_command}")
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Successfully updated the local save file.")
    else:
        print(f"Failed to update the local save file. Error: {result.stderr}")

def cleanup_remote_tmp_path():
    """Cleans up the temporary file on the Android device."""
    adb_command = f"adb shell rm -r {REMOTE_TMP_PATH}"
    print(f"Executing: {adb_command}")
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Successfully cleaned up the temporary file.")
    else:
        print(f"Failed to clean up the temporary file. Error: {result.stderr}")

def main():
    bucket_name = "save_files"
    user_id = input("Enter your user ID (as a number): ")
    destination_path = f"{user_id}/meta.jkr"
    isDownload = input("Do you want to download your save file from the database or upload your save to the database? (d/u): ").strip().lower()

    if isDownload == "d":
        try:
            # Fetch the file from the storage bucket
            data = supabase.storage.from_(bucket_name).download(destination_path)
            if data:
                with open(LOCAL_TMP_PATH, "wb") as file:
                    file.write(data)
                adb_push_command = f"adb push {LOCAL_TMP_PATH} {REMOTE_TMP_PATH}"
                result = subprocess.run(adb_push_command, shell=True, capture_output=True, text=True)
                update_local_save_file()
            else:
                print("Failed to download the file. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cleanup_remote_tmp_path()
    elif isDownload == "u":
        try:
            pull_file_with_adb()
            update_file_from_bucket(bucket_name, REMOTE_TMP_PATH, destination_path)
            print("File uploaded successfully!")
        except subprocess.CalledProcessError as e:
            print(f"ADB command failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Cleanup local temp file
            cleanup_remote_tmp_path()
    else:
        print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
