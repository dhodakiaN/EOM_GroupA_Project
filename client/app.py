import os  # Importing os module to interact with the OS and file system
from dotenv import load_dotenv  # Importing load_dotenv function from dotenv package to load environment variables
import socket  # Importing socket module for network connections
from menu import launchMenu  # Importing launchMenu function from menu module


def runApp():
    """
    Loads the environment variables and launches the menu.
    """
    load_dotenv()  # Loading environment variables from a .env file
    launchMenu()  # Launching the menu


if __name__ == '__main__':
    # Checking if the script is being run as the main module,
    # and if so, calling the runApp function to start the application
    runApp()
