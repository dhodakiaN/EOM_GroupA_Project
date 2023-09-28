from helpers import error_message, clear_screen, forced_input
from actions import login, create_account

def launchMenu(connection):
      clear_screen()
      files_list = []
      email, username = '', ''

      while True:  # Keep running the loop until a break statement is encountered
            try:
                  email, username = login(connection)
                  if bool(username) and bool(email):
                        print(f'Welcome {username} ({email}) to the file sharing system')
                        print('1. Upload File.')
                        print('2. Download File.')
                        print('0. Exit.')
                        option = input('What Would You Like To Do : ')
                        try:
                              option = int(option)
                        except ValueError:  # Catch ValueError when converting input to int
                              error_message('Invalid Option')
                              continue  # Continue to the next iteration of the loop
                        if option not in range(0, 3):
                              error_message('Invalid Option')
                              continue  # Continue to the next iteration of the loop
                        elif option == 0:
                              clear_screen()
                              print('Thanks for using the file sharing system')
                              break  # Exit the loop
                        elif option == 1:
                              pass  # Handle file upload
                        elif option == 2:
                              pass  # Handle file download
                        else:
                              print('Try again')
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


