import os  # For interacting with the operating system
import uuid  # For generating unique identifiers
from time import sleep  # For pausing the execution of the program
import socket  # For creating network connections
import rsa  # for encryption


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
    # clear_screen()
    print(f'\n\033[1;31m{message}\033[0m\n')  # \033[1;31m and \033[0m are used to color the text red
    sleep(3)  # Pauses execution for 3 seconds
    # clear_screen()


def success_message(message):
    """
    Displays a success message to the user and clears the screen after a short delay.

    :param message: The success message to be displayed.
    """
    # clear_screen()
    print(f'\n\033[1;32m{message}\033[0m\n')  # \033[1;32m and \033[0m are used to color the text green
    sleep(3)  # Pauses execution for 3 secondsfdg
    # clear_screen()


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


def encrypt_data(data, public_key):
    try:
        # Encrypt the data using the public key
        encrypted_data = rsa.encrypt(data, public_key)
        return encrypted_data
    except Exception as e:
        print(e)
        return None


def loadpublickey(public_key):
    # Load the public key into an RSA key object
    public_key = rsa.PublicKey.load_pkcs1(public_key, format='PEM')
    return public_key
