import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_unique_bigint():
    """Generates a unique BIGINT identifier."""
    while True:
        new_id = random.randint(1, 9223372036854775807)  # Max value for BIGINT
        # Check if the ID already exists in the database
        result = supabase.table("Saves").select("id").eq("id", new_id).execute()
        if not result.data:  # If no data is returned, the ID is unique
            return new_id

def upload_file_to_bucket(bucket_name: str, file_path: str, destination_path: str, user_id):
    """Uploads a file to the specified storage bucket."""
    with open(file_path, "rb") as file:
        response = supabase.storage.from_(bucket_name).upload(file=file, path=destination_path)
    
        return supabase.storage.from_(bucket_name).list(str(user_id))[0]["id"]  # Return the id of the uploaded file
    
def update_file_from_bucket(bucket_name: str, file_path: str, destination_path: str):
    """Updates a file of the specified storage bucket."""
    with open(file_path, "rb") as file:
        return supabase.storage.from_(bucket_name).update(file=file, path=destination_path)        

def main():
    bucket_name = "save_files"

    isDownload = input("Do you want to download a save file or upload a save file? (d/u): ").strip().lower()

    if isDownload == "d":
        user_id = input("Enter your user ID (as a number): ")
        path = input("Enter the file path where to update your save file (eg. C:\\Users\\User\\AppData\\Roaming\\Balatro\\1\\meta.jkr): ")
        destination_path = f"{user_id}/meta.jkr" # File path in storage bucket

        try:
            # Fetch the file from the storage bucket
            data = supabase.storage.from_(bucket_name).download(destination_path)
            if data:
                with open(path, "wb") as file:
                    file.write(data)
                print("File downloaded successfully!")
            else:
                print("Failed to download the file. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
    elif isDownload == "u":
        response = input("Do you already have a save in the database? (y/n): ").strip().lower()

        if response == "y":
            user_id = input("Enter your user ID (as a number): ")
            if not user_id.isdigit():
                print("Invalid user ID. Must be a number.")
                return

            file_path = input("Enter the file path to your save file (eg. C:\\Users\\User\\AppData\\Roaming\\Balatro\\1\\meta.jkr): ")
            file_name = os.path.basename(file_path)
            destination_path = f"{user_id}/{file_name}"

            try:
                # Fetch the existing file key from the database
                result = supabase.table("Saves").select("file_key").eq("id", int(user_id)).execute()
                if result.data:
                    # Update the file from the storage bucket
                    data = update_file_from_bucket(bucket_name, file_path, destination_path)
                    if data != None:
                        print("File uploaded and database updated successfully!")
                        public_url = supabase.storage.from_(bucket_name).get_public_url(destination_path)
                        print("Public URL:", public_url)
                    else:
                        print("Failed to update the database.")
                else:
                    print("No record found for the given user ID.")
            except Exception as e:
                print(f"Error: {e}")

        elif response == "n":
            # Generate a unique BIGINT user ID
            user_id = generate_unique_bigint()
            file_path = input("Enter the file path to your save file (eg. C:\\Users\\User\\AppData\\Roaming\\Balatro\\1\\meta.jkr): ")
            file_name = os.path.basename(file_path)
            destination_path = f"{user_id}/{file_name}"  # File path in storage bucket

            try:
                # Upload the file to the storage bucket
                file_key = upload_file_to_bucket(bucket_name, file_path, destination_path, user_id)

                # Insert a new record into the database with the user ID and file's storage key
                data = supabase.table("Saves").insert({"id": user_id, "file_key": file_key}).execute()
                if data.data:
                    print(f"New save added successfully! Your user ID is: {user_id}")
                    print("Make sure to note down your user ID for future reference.")
                    public_url = supabase.storage.from_(bucket_name).get_public_url(destination_path)
                    print("Public URL:", public_url)
                else:
                    print("Failed to add a new save. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid response. Please type 'y' or 'n'.")

if __name__ == "__main__":
    main()
