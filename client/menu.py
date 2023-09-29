import socket  # For creating network connections
import os  # For interacting with the operating system
# For displaying file and directory selection dialogs
from tkinter.filedialog import askopenfilename, askdirectory

# Importing various helper functions and actions
from helpers import error_message, success_message, clear_screen, forced_input, create_connection
from actions import login, create_account, send_file_to_server, download_file_from_server, get_files_list


def launchMenu():
    """
    Launches the main menu of the application allowing the user to interact with the file sharing system.
    """
    clear_screen()  # Clearing the console screen
    
    files_list = []  # Initializing the list of files

    connection = create_connection()  # Creating a new socket connection
    # Logging in and getting email and username
    authrized, email, username = login(connection)
        

    connection.close()  # Closing the connection after login

    while True:  # Main loop to keep the menu running
        try:
            if connection:
                connection.close()  # Closing the connection if it is open
            connection = create_connection()  # Creating a new connection for each iteration
            if authrized:  # Checking if user is logged in
                print(
                    f'Welcome {username} ({email}) to the file sharing system')
                print('1. Upload File.')
                print('2. Download File.')
                print('0. Exit.')
                option = input('What Would You Like To Do : ')
                if option == '1':  # Upload File
                    file_path = askopenfilename()  # Displaying file selection dialog
                    if not file_path:
                        error_message('File not selected')
                        continue

                    if send_file_to_server(connection, file_path):
                        success_message('File uploaded successfully')
                    else:
                        error_message('Error While Uploading File')

                elif option == '2':  # Download File
                    clear_screen()
                    # Getting the list of available files
                    files_list = get_files_list(connection)

                    if not files_list:
                        error_message('No files found')
                        continue

                    # Displaying the list of files
                    for index, file in enumerate(files_list):
                        print(f'({index + 1}) {file}')
                    selected_file_index = int(forced_input(
                        'Please enter the file number (enter 0 to cancel) : '))
                    if selected_file_index == 0:
                        continue
                    if selected_file_index > len(files_list):
                        error_message('Invalid file number')
                        continue

                    selected_file_name = files_list[selected_file_index - 1]
                    selected_directory = askdirectory()  # Displaying directory selection dialog
                    if not selected_directory:
                        error_message('Directory not selected')
                        continue

                    connection.close()  # Closing and reopening the connection before downloading the file
                    connection = create_connection()

                    if download_file_from_server(connection, selected_file_name, selected_directory):
                        success_message('File downloaded successfully')
                    else:
                        error_message('Error While Downloading File')

                elif option == '0':  # Exit
                    clear_screen()
                    print('Thank you for using our system')
                    break  # Exiting the main loop

                else:
                    error_message('Invalid Option, please try again')
            else:  # Create an Account
                print('This is your first time using our system in this device')
                print('Please Create an account first')
                email = forced_input('Email : ')
                username = forced_input('Username : ')
                create_account(
                    connection, {'email': email, 'username': username})
                connection.close()  # Closing the connection after account creation
                clear_screen()
                authrized = True

        except Exception as e:  # Handling any unexpected exceptions
            error_message(str(e))
            connection.close()  # Closing the connection in case of an error

    connection.close()  # Closing the connection when exiting the application
