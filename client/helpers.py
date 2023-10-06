import os  # For interacting with the operating system
import uuid  # For generating unique identifiers
from time import sleep  # For pausing the execution of the program
import socket  # For creating network connections
from cryptography.fernet import Fernet # Import Encryption 


def forced_input(message):
    """
    Keeps prompting the user to input a value until a non-empty string is entered.

    :param message: The message to display to the user when prompting for input.
    :return: The non-empty string entered by the user.
    """
    while True:
        response = input(message)
        if response != "":
            return response


def clear_screen():
    """
    Clears the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' for Windows, 'clear' for others


def error_message(message):
    """
    Displays an error message to the user and clears the screen after a short delay.

    :param message: The error message to be displayed.
    """
    clear_screen()
    print(f'\n\033[1;31m{message}\033[0m\n')  # \033[1;31m and \033[0m are used to color the text red
    sleep(3)  # Pauses execution for 3 seconds
    clear_screen()


def success_message(message):
    """
    Displays a success message to the user and clears the screen after a short delay.

    :param message: The success message to be displayed.
    """
    #clear_screen()
    print(f'\n\033[1;32m{message}\033[0m\n')  # \033[1;32m and \033[0m are used to color the text green
    sleep(3)  # Pauses execution for 3 secondsfdg
    #clear_screen()


def get_mac_address():
    """
    Returns the MAC address of the computer.

    :return: The MAC address as a string.
    """
    # Formatting and joining the MAC address parts in reverse order
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])


def to_request(event, data={}):
    """
    Converts an event and associated data to a string and encodes it to bytes.

    :param event: The event type as a string.
    :param data: The associated data as a dictionary.
    :return: The encoded string representation of the event and data.
    """
    return str({'event': event, 'data': data}).encode('utf-8')


def create_connection():
    """
    Creates and returns a new socket connection to the server specified by HOST and PORT environment variables.

    :return: The socket connection object.
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a new socket object
    # Connecting to the server using the HOST and PORT specified in the environment variables
    connection.connect((os.getenv('HOST'), int(os.getenv('PORT'))))
    return connection


def generate_key():
    """
    Generate a key and save it to a file for later decryption.
    If the key already exists, it does nothing.
    """
    key_path = "./client/assets/key.key"
    
    # Check if key file already exists
    if os.path.exists(key_path):
        print("Key already exists. No new key was generated.")
        return
    
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print("New key generated and saved.")

def load_key():
    """
    Load the previously generated key from the key file.
    """
    return open("./client/assets/key.key", "rb").read()

def encrypt_file(file_path):
    """
    Encrypt the given file using the provided key and save it as a new encrypted file.
    
    Returns the path of the encrypted file.
    """
    key = load_key()
    cipher = Fernet(key)

    # Read the original file
    with open(file_path, "rb") as file:
        original_data = file.read()

    # Encrypt the data
    encrypted_data = cipher.encrypt(original_data)

    # Create a new filename for the encrypted file with the _encr suffix
    base, extension = os.path.splitext(file_path)
    encrypted_file_path = f"{base}_encr{extension}"

    # Write the encrypted data to the new file
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)

    print("File encrypted successfully!")
    
    return encrypted_file_path  # Return the path of the encrypted file

def decrypt_file(file_path):
    """
    Decrypt the given file using the provided key.
    """
    key = load_key()
    cipher = Fernet(key)

    # Read the encrypted file
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)
    print("this is encrypted ")
    print(encrypted_data)
    print("this is decrypted data")
    print(decrypted_data)
    # Write the decrypted data back to the file
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

    print("File decrypted successfully!")