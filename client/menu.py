import socket
import os
from tkinter.filedialog import askopenfilename, askdirectory

from helpers import error_message, success_message, clear_screen, forced_input, create_connection
from actions import login, create_account, send_file_to_server, download_file_from_server, get_files_list

def launchMenu():
      clear_screen()
      email, username = '', ''
      files_list = []

      connection = create_connection()
      email, username = login(connection)
      connection.close()



      while True:
            try:
                  if connection:
                        connection.close()
                  connection = create_connection()
                  if bool(username) and bool(email):
                        print(f'Welcome {username} ({email}) to the file sharing system')
                        print('1. Upload File.')
                        print('2. Download File.')
                        print('0. Exit.')
                        option = input('What Would You Like To Do : ')
                        if option == '1':

                              file_path = askopenfilename()
                              if not file_path:
                                    error_message('File not selected')
                                    continue

                              if send_file_to_server(connection, file_path):
                                    success_message('File uploaded successfully')
                              else:
                                    error_message('Error While Uploading File')

                        elif option == '2':
                              clear_screen()
                              files_list = get_files_list(connection)

                              if not files_list:
                                    error_message('No files found')
                                    continue

                              for index, file in enumerate(files_list):
                                    print(f'({index + 1}) {file}')
                              selected_file_index = int(forced_input('Please enter the file number (enter 0 to cancel) : '))
                              if selected_file_index == 0:
                                    continue
                              if selected_file_index > len(files_list):
                                    error_message('Invalid file number')
                                    continue

                              selected_file_name = files_list[selected_file_index - 1]
                              selected_directory = askdirectory()
                              if not selected_directory:
                                    error_message('Directory not selected')
                                    continue

                              connection.close()
                              connection = create_connection()

                              if download_file_from_server(connection, selected_file_name, selected_directory):
                                    success_message('File downloaded successfully')
                              else:
                                    pass
                                    # error_message('Error While Downloading File')



                        elif option == '0':
                              clear_screen()
                              print('Thank you for using our system')
                              break

                        else:
                              error_message('Invalid Option, please try again')
                  else:
                        # Let's create an account
                        print('This is your first time using our system in this device')
                        print('Please Create an account first')
                        email = forced_input('Email : ')
                        username = forced_input('Username : ')
                        create_account(connection, {
                              'email': email,
                              'username': username
                        })


            except Exception as e:
                  error_message(str(e))
                  connection.close()


      connection.close()
