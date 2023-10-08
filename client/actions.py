import os  # Importing os module to interact with the OS and file system
import pickle  # importing pickle module to pickle
import json  # import module for json files
import dicttoxml  # import module for xml files
from helpers import clear_screen, forced_input, to_request, get_mac_address, encrypt_data, create_connection
import socket  # Importing socket module for network connections
import rsa
import xml.etree.ElementTree as ET


def create_account(connection, data):
    """
    Sends a request to create a new account.

    :param connection: The socket connection object.
    :param data: A dictionary containing 'email' and 'username' of the user.
    :return: True if account is created successfully, False otherwise.
    """
    try:
        mac_address = get_mac_address()  # Getting MAC address of the user's machine
        email, username = data['email'], data['username']  # Extracting email and username from the data parameter
        # Sending a signup request with mac_address, email, and username
        connection.send(to_request('signup', {
            'mac_address': mac_address,
            'email': email,
            'username': username
        }))
        return True
    except Exception as e:  # Handling exceptions
        connection.send('account-not-created'.encode('utf-8'))  # Sending error message if account creation fails
        return False


def login(connection):
    """
    Sends a login request and receives the response.

    :param connection: The socket connection object.
    :return: A tuple containing 'email' and 'username' if authorized, False otherwise.
    """
    try:
        mac_address = get_mac_address()  # Getting MAC address of the user's machine
        # Sending a login request with mac_address
        connection.send(to_request('login', {'mac_address': mac_address}))
        response = connection.recv(1024).decode('utf-8')  # Receiving and decoding response

        if response == 'not-authorized':
            print('Not authorized')
            return False, '', ''

        response = eval(response)  # Evaluating the response string to convert it to a Python object
        return True, response['email'], response['username']

    except Exception as e:
        print(e)
        return False, '', ''


def get_files_list(connection):
    """
    Sends a request to get the list of files and receives the response.

    :param connection: The socket connection object.
    :return: A list containing file information if successful, empty list otherwise.
    """
    try:
        connection.send(to_request('get-files', {}))  # Sending a get-files request
        response = connection.recv(1024).decode('utf-8')  # Receiving and decoding response

        if response == 'invalid-request':
            raise Exception('Invalid request')  # Raising exception if response is 'invalid-request'

        return eval(response)  # Evaluating the response string to convert it to a Python object
    except Exception as e:  # Handling exceptions
        print(e)
        return []


def download_file_from_server(connection, file_name, directory_path):
    """
    Sends a request to download a file from the server.

    :param connection: The socket connection object.
    :param file_name: The name of the file to be downloaded.
    :param directory_path: The path of the directory where the downloaded file will be saved.
    :return: True if file is downloaded successfully, False otherwise.
    """
    try:
        # Sending a download-file request with file_name
        connection.send(to_request('download-file', {'name': file_name}))
        response = connection.recv(65536).decode('utf-8')  # Receiving and decoding response

        if response == 'file-not-found':
            raise Exception('File not found')  # Raising exception if file is not found

        file_path = os.path.join(directory_path, file_name)  # Creating the full file path
        with open(file_path, 'wb') as file:  # Using a context manager to handle the file operations
            file.write(eval(response))  # Writing the evaluated response to the file
        return True
    except Exception as e:  # Handling exceptions
        print(e)
        print('File not downloaded')
        return False


def send_file_to_server(connection, file_path):
    """
    Sends a file to the server.

    :param connection: The socket connection object.
    :param file_path: The path of the file to be sent.
    :return: True if file is sent successfully, False otherwise.
    """
    try:
        file = open(file_path, 'rb')  # Opening the file in binary read mode
        file_name = os.path.basename(file_path)  # Getting the base name of the file
        file_size = os.path.getsize(file_path)  # Getting the size of the file
        file_data = file.read(file_size)  # Reading the content of the file
        # Sending an upload-file request with file_data, file_name, and file_size
        connection.send(to_request('upload-file', {
            'bytes': file_data,
            'name': file_name,
            'size': file_size
        }))

        file.close()  # Closing the file
        return True
    except Exception as e:  # Handling exceptions
        print(e)
        return False


def request_public_key_from_server(connection):
    """
    Requests the public key from the server.

    :param connection: The socket connection object.
    :return: Public key as a byte string if received successfully, None otherwise.
    """
    try:
        # Sending a request to the server to get the public key
        request = {
            'event': 'request-public-key',
            'data': "sendpublickey"
        }
        connection.send(str(request).encode('utf-8'))
        # Receive the public key from the server
        public_key = connection.recv(65536)
        return public_key
    except Exception as e:
        print(e)
        return None


def screenprint(connection, data_dict, encryptdata, public_key=None):
    try:
        if encryptdata == False:
            connection.send(to_request('Screenprint', data_dict))
            return True
        elif encryptdata == True:
            data_to_encrypt = pickle.dumps(data_dict)
            encrypted_data = encrypt_data(data_to_encrypt, public_key)
            connection.send(to_request('Screenprintenc', encrypted_data))
            return True
    except Exception as e:  # Handling exceptions
        print(e)
        return False


def pickling_Binary(data_dict, filename, encryptdata, public_key=None):
    directory = './client/assets/'
    filepath = os.path.join(directory, filename + '.pkl')
    print(data_dict, filename, encryptdata, public_key)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if encryptdata and public_key is not None:
        # Serialize the data_dict to a binary string
        data_to_encrypt = pickle.dumps(data_dict)

        # Encrypt the data using the public key
        encrypted_data = encrypt_data(data_to_encrypt, public_key)

        # Write the encrypted data to the file
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
    else:
        # Serialize and write the data_dict as is (not encrypted)
        with open(filepath, 'wb') as file:
            pickle.dump(data_dict, file)

    return filepath


def pickling_JSON(data_dict, filename, encryptdata, public_key=None):
    directory = './client/assets/'
    filepath = os.path.join(directory, filename + '.json')

    if not os.path.exists(directory):
        os.makedirs(directory)

    if encryptdata and public_key is not None:
        # Serialise the data_dict to a JSON string
        data_to_encrypt = json.dumps(data_dict)
        encoded_data = data_to_encrypt.encode('utf-8')  # needs additional encodeing
        # Encrypt the data using the public key
        encrypted_data = encrypt_data(encoded_data, public_key)

        # Write the encrypted data to the file
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
    else:
        # Serialize and write the data_dict as JSON (not encrypted)
        with open(filepath, 'w') as file:
            json.dump(data_dict, file)

    return filepath


def pickling_XML(data_dict, filename, encryptdata, public_key=None):
    xml_data = dicttoxml.dicttoxml(data_dict)
    directory = './client/assets/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename + '.xml')

    if encryptdata and public_key is not None:
        # Encrypt the XML data using the public key
        encrypted_data = encrypt_data(xml_data, public_key)

        # Write the encrypted data to the file
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
    else:
        # Write the XML data as is (not encrypted)
        with open(filepath, 'wb') as file:
            file.write(xml_data)

    return filepath
