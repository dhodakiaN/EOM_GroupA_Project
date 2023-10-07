import socket  # For creating network connections
import os  # For interacting with the operating system
# For displaying file and directory selection dialogs
from tkinter.filedialog import askopenfilename, askdirectory

# Importing various helper functions and actions
from helpers import error_message, success_message, clear_screen, forced_input, create_connection,encrypt_data,loadpublickey
from actions import login, create_account, send_file_to_server, download_file_from_server, get_files_list,pickling_Binary,pickling_JSON,pickling_XML,screenprint,request_public_key_from_server


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
                print(f'Welcome {username} ({email}) to groups A system')
                print('1. Create a dictionary, populate it, serialize it and send it to a server..')
                print('2. Create a text file and send it to a server')
                print('0. Exit.')
                optionsystem = input('What Would You Like To Do from Above Options: ')
                if optionsystem =="1":
                    print("This is the dictionary system")
                    dictkey = input('Can you please populate the key to the dictionary? ')
                    dictvalues = input('Can you please populate the values to the dictionary? ')
                    userdictionary={dictkey:dictvalues}
                    print("This is your dictionary below:")
                    print(userdictionary)
                    print("Do you want to encrypt the data before it is sent to a server?")
                    print('1. Yes')
                    print('2. No')
                    optionencrypt = input('What Would You Like To Do from the Above Options: ')
                    if optionencrypt == "1":
                        public_key = request_public_key_from_server(connection)
                        public_key = loadpublickey(public_key)
                        connection.close()
                        connection = create_connection()
                        encryptdata=True #flag to encrypt data
                    elif optionencrypt == "2":
                        encryptdata=False #flag to keep data the same
                    print("Do you want the server to print or do you want to save the data in a file?")
                    print('1. Print the contents to a screen in the server')
                    print('2. Save the contents to a file')
                    print('0. Exit.')
                    optionconfserver = input('What Would You Like To Do from the Above Options: ')
                    if optionconfserver == "1" and encryptdata==False :
                        if screenprint(connection,userdictionary,encryptdata):
                            success_message('Printed on Server Successfully')
                            break
                        else:
                            error_message('Error While Printing on Server')
                    elif optionconfserver == "1" and encryptdata==True :
                        #code for print screen and encrypt
                        if screenprint(connection,userdictionary,encryptdata,public_key):
                            success_message('Encrypted data sent Successfully')
                            break
                        else:
                            error_message('Error While Printing on Server')
                    elif optionconfserver == "2":
                        dictfilename  = input('Please Enter the Desired File Name:  ')
                    elif optionconfserver == "0":
                        print("Exiting system")
                        break
                    print("In what pickling format do you want to serialise the data and then send to server")
                    print('1. Binary')
                    print('2. JSON')
                    print('3. XML')
                    optionpicklingformat= input('What Would You Like To Do from Above Options: ')
                    if optionpicklingformat == "1":
                        file_path = pickling_Binary(userdictionary, dictfilename,encryptdata,public_key)
                        if send_file_to_server(connection, file_path):
                            success_message('File uploaded successfully')
                        else:
                            error_message('Error While Uploading File')
                    elif optionpicklingformat == "2":
                        file_path = pickling_JSON(userdictionary, dictfilename,encryptdata,public_key)
                        if send_file_to_server(connection, file_path):
                            success_message('File uploaded successfully')
                        else:
                            error_message('Error While Uploading File')
                    elif optionpicklingformat == "3":         
                        file_path = pickling_XML(userdictionary,dictfilename,encryptdata,public_key)
                        if send_file_to_server(connection, file_path):
                            success_message('File uploaded successfully')
                        else:
                            error_message('Error While Uploading File')
                elif optionsystem == "2":
                    print('This is the file sharing system')
                    print('1. Upload File.')
                    print('2. Upload File and Encrypt')
                    print('3. Download File.')
                    print('4. Create a text file.')
                    print('0. Exit.')
                    option = input('What Would You Like To Do from Above Options: ')
                    if option == '1':  # Upload File
                        print("New Window Opened, Select the .txt file to send")
                        file_path = askopenfilename()  # Displaying file selection dialog
                        if not file_path:
                            error_message('File not selected')
                            continue
                        if send_file_to_server(connection, file_path):
                            success_message('File uploaded successfully')
                        else:
                            error_message('Error While Uploading File')
                    
                    elif option == '2':  # Upload file and encrypt
                        print("New Window Opened, Select the .txt file to send")
                        file_path = askopenfilename()  # Displaying file selection dialog
                        if not file_path:
                            error_message('File not selected')
                            continue
                        public_key = request_public_key_from_server(connection)
                        public_key = loadpublickey(public_key)
                        connection.close()
                        connection = create_connection()
                        # Read the contents of the text file
                        with open(file_path, 'rb') as file:
                            file_contents = file.read()
                        encrypted_contents = encrypt_data(file_contents, public_key)
                        with open(file_path, 'wb') as file:
                            file.write(encrypted_contents)
                        
                        # Attempt to send the encrypted file (with the _encr suffix) to the server
                        if send_file_to_server(connection, file_path):
                            success_message('File uploaded and encrypted successfully')
                        else:
                            error_message('Error While Uploading File')


                    elif option == '3':  # Download File
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
                        print("New Window Opened, Select the Directory for Download from Server")
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

                    elif option == '4':  # Enter text and send text file to server
                        textdata = input("Please enter the text for the text file: \n")
                        textfilename = input("Please enter the file name for the text file without the extension: \n")
                        pathclient='./client/assets/'+textfilename+".txt"
                        # Create and write the text data to a text file
                        with open(pathclient, 'w') as textfile:
                            textfile.write(textdata) # create client side file
                        print(f"Text data has been written to {textfilename}")
                        print("Do you want to encrypt the data before it is sent to a server?")
                        print('1. Yes')
                        print('2. No')
                        optionencrypt = input('What Would You Like To Do from the Above Options: ')
                        if optionencrypt == "1":
                            public_key = request_public_key_from_server(connection)
                            public_key = loadpublickey(public_key)
                            connection.close()
                            connection = create_connection()
                            encryptdata=True #flag to encrypt data
                        elif optionencrypt == "2":
                            encryptdata=False #flag to encrypt data
                        print("Do you want the server to print or do you want to save the data in a file?")
                        print('1. Print the contents to a screen in the server')
                        print('2. Save the contents to a file')
                        print('0. Exit.')
                        optionconfserver = input('What Would You Like To Do from the Above Options: ')
                        if optionconfserver == "1" and encryptdata==False :
                            if screenprint(connection,textdata,encryptdata):
                                success_message('Printed on screen')
                                break
                            else:
                                error_message('Error While Printing on Server')
                        elif optionconfserver == "1" and encryptdata==True :
                            #code for print screen and encrypt
                            if screenprint(connection,textdata,encryptdata,public_key):
                                success_message('Encrypted Data sent Successfully')
                                break
                            else:
                                error_message('Error While Printing on Server')
                        elif optionconfserver == "2" and encryptdata==False :

                            if send_file_to_server(connection, pathclient):
                                success_message('File uploaded successfully')
                            else:
                                error_message('Error While Uploading File')

                        elif optionconfserver == "2" and encryptdata==True :
                            # Read the contents of the text file
                            with open(pathclient, 'rb') as file:
                                file_contents = file.read()
                            encrypted_contents = encrypt_data(file_contents, public_key)
                            with open(pathclient, 'wb') as file:
                                file.write(encrypted_contents)
                            
                            if send_file_to_server(connection, pathclient):
                                success_message(' Encrypted File uploaded successfully')
                            else:
                                error_message('Error While Uploading File')

                        elif optionconfserver == "0":
                            print("Exiting system")
                            break

                    

                    elif option == '0':  # Exit
                        clear_screen()
                        print('Thank you for using our system')
                        break  # Exiting the main loop

                    else:
                        error_message('Invalid Option, please try again')
                elif optionsystem == "0":
                    print("Exiting system")
                    break
                else:
                    print("Unrecognised input exiting")
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
