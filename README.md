# Balatro Save Manager

Balatro Save Manager is a tool that allows you to upload and retrieve your save files from your computer and mobile device without needing to plug in your mobile device. This project uses Supabase for storage and database management.

Unfortunately, this save manager does not work with IOS devices.

## Warnings
Balatro Save Manager is not very secure since it requires you to have wireless debugging enabled on your phone.

Also, the setup on mobile is not very user friendly, so I only recommend it for users with some experience.

## Features

- Upload save files from your computer or mobile device to the cloud.
- Download save files from the cloud to your computer or mobile device.
- Generate unique user IDs for new save files.
- Update existing save files in the cloud.

## Requirements

- Python 3.6+
- Supabase account with a configured project
- ADB (Android Debug Bridge) for mobile device operations
- Environment variables for Supabase URL and API key
- Termux installed on your Android device
- USB Debugging enabled on your Android device

## Options for users
There are two different options available to users
1. You can use a database I have made that is already setup and available to everyone but will require you to remember your user id to access your save file.
2. You can create and use your own database. For this you will need to change the values of these two environment variables.
   ```env
   SUPABASE_URL
   SUPABASE_KEY
   BUCKET_NAME
   ```

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/balatro-save-manager.git
    cd balatro-save-manager
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Computer

1. Run the [Balatro_Save_Manager.py](https://github.com/OliBigo/balatro-save-manager/blob/main/Balatro_Save_Manager.py) script or download and execute one of the [executables](https://github.com/OliBigo/balatro-save-manager/releases):
    ```sh
    python Balatro_Save_Manager.py
    ```

2. Follow the prompts to upload or download your save file.

### Mobile

1. Open Termux and execute the following commands:
   ```sh
   pkg update
   pkg install python
   pkg install android-tools
   ```

2. Connect your phone to your computer via USB, enable USB debugging on your phone and enable Wifi debugging on your phone
   
3. Run the following commands on the terminal of your computer:
   ```sh
   adb devices
   adb kill-server
   adb start-server
   adb tcpip 5555
   ```

4. Find the IP address and port of your phone for Wifi debugging
5. Run the following command in Termux on your phone (make sure to change <IP Address> and <Port> with the values you found during step 4):
   ```sh
   adb connect <IP Address>:<Port>
   ```

6. Download the [Save_Manager_Mobile.py](https://github.com/OliBigo/balatro-save-manager/blob/main/Save_Manager_Mobile.py) and open it with Termux. Then run it with the following command in Termux:
    ```sh
    python Save_Manager_Mobile.py
    ```

7. Follow the prompts to upload or download your save file.
8. Once you are done transferring the files make sure you disconnect ADB with the following command in Termux:
   ```sh
   adb disconnect
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/OliBigo/balatro-save-manager/blob/main/LICENSE) file for details.

## Contributing

Contributions and ideas on how to improve this save file manager are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Supabase](https://supabase.io/) for providing the backend services.
- [Python](https://www.python.org/) for the programming language.
- [ADB](https://developer.android.com/studio/command-line/adb) for Android device management.
- [Termux](https://termux.dev/en/) for the command line that allows the mobile save file manager to work
