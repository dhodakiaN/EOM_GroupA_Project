# Importing helper functions
from helpers import load_account, save_account, all_files, create_file, get_file_bytes


def check_account(connection, data):
    """
    Checks whether an account associated with the given MAC address exists and sends the account information or
    an error message back through the connection.

    :param connection: The socket connection object.
    :param data: A dictionary containing the 'mac_address' to check.
    """
    try:
        accounts = load_account()  # Loading existing accounts
        mac_address = data['mac_address']  # Extracting MAC address from data
        if mac_address in accounts:  # Checking if the MAC address is in the accounts
            # Sending account information if found
            connection.send(str(accounts[mac_address]).encode('utf-8'))
        else:
            # Raising exception if MAC address is not found
            raise Exception('Not authorized')
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        # Sending 'not-authorized' message in case of an error
        connection.send('not-authorized'.encode('utf-8'))


def create_account(connection, data):
    """
    Creates a new account with the given information and sends a confirmation or an error message back through the connection.

    :param connection: The socket connection object.
    :param data: A dictionary containing the 'mac_address', 'email', and 'username' for the new account.
    """
    try:
        # Formatting account information
        account = {data['mac_address']: {
            'email': data['email'], 'username': data['username']}}
        if save_account(account):  # Saving the new account information
            # Sending confirmation message if successful
            connection.send('account-created'.encode('utf-8'))
        else:
            # Raising exception if account is not created
            raise Exception('Account not created')
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        # Sending error message in case of an error
        connection.send('account-not-created'.encode('utf-8'))


def get_files(connection):
    """
    Sends the list of all files back through the connection.

    :param connection: The socket connection object.
    """
    files = all_files()  # Getting the list of all files
    connection.send(str(files).encode('utf-8'))  # Sending the list of files


def upload_file(connection, data):
    """
    Uploads a file with the given name and bytes and sends a confirmation or an error message back through the connection.

    :param connection: The socket connection object.
    :param data: A dictionary containing the 'name' and 'bytes' for the file to be uploaded.
    """
    
    try:
        # Creating a new file with the received name and bytes
        if create_file(data['name'], data['bytes']):
            # Sending confirmation message if successful
            connection.send('file-uploaded'.encode('utf-8'))
        else:
            # Raising exception if file is not uploaded
            raise Exception('File not uploaded')
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        # Sending error message in case of an error
        connection.send('file-not-uploaded'.encode('utf-8'))


def download_file(connection, data):
    """
    Downloads a file with the given name and sends the file bytes or an error message back through the connection.

    :param connection: The socket connection object.
    :param data: A dictionary containing the 'name' of the file to be downloaded.
    """
    try:
        # Getting the bytes of the file with the given name
        file_bytes = get_file_bytes(data['name'])
        if file_bytes:  # Checking if file bytes are successfully received
            # Sending the file bytes if successful
            connection.send(str(file_bytes).encode('utf-8'))
        else:
            # Raising exception if file is not found
            raise Exception('File not found')
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        # Sending error message in case of an error
        connection.send('file-not-found'.encode('utf-8'))

def request_public_key(connection,public_key):
    try:    
        if public_key:
            # Send the public key to the client
            connection.send(public_key.save_pkcs1(format="PEM"))
            connection.close()
        else:
            # Handle the case where the public key is not found
            connection.send("Public key not found".encode('utf-8'))
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        # Sending error message in case of an error
        connection.send('public-key-not-found'.encode('utf-8'))
