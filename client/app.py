import os
from dotenv import load_dotenv
import socket
from menu import launchMenu

def runApp():
    load_dotenv()
    launchMenu()


if __name__ == '__main__':
    runApp()
