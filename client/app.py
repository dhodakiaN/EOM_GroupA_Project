import os
from dotenv import load_dotenv
import socket
from helpers import get_mac_address, to_request
from actions import send_file_to_server, download_file_from_server, login
from menu import launchMenu

def runApp():
    load_dotenv()
    mac_address = get_mac_address()
    connection = socket.socket()
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    connection.connect((host, port))
    launchMenu(connection)


if __name__ == '__main__':
    runApp()
    