import os
from helpers import clear_screen, forced_input, to_request, get_mac_address
import socket


def create_account(connection, data):
    try:
        mac_address = get_mac_address()
        email, username = data['email'], data['username']
        connection.send(to_request('signup', {
            'mac_address': mac_address,
            'email': email,
            'username': username
        }))
        return True
    except Exception as e:
        connection.send('account-not-created'.encode('utf-8'))
        return False

def login(connection):
    mac_address = get_mac_address()
    connection.send(to_request('login', {
        'mac_address': mac_address
    }))

    response = connection.recv(1024).decode('utf-8')

    if response == 'not-authorized':
        print('Not authorized')
        return False

    response = eval(response)
    return response['email'], response['username']


def get_files_list(connection):
    try:
        connection.send(to_request('get-files', {}))
        response = connection.recv(1024).decode('utf-8')
        if response == 'invalid-request':
            raise Exception('Invalid request')
        return eval(response)
    except Exception as e:
        print(e)
        return []

def download_file_from_server(connection, file_name, directory_path):
    try:
        connection.send(
            to_request('download-file', {
                'name': file_name
            })
        )

        # 2^16 = 65536
        response = connection.recv(65536).decode('utf-8')

        if response == 'file-not-found':
            raise Exception('File not found')

        file_path = os.path.join(directory_path, file_name)
        file = open(file_path, 'wb')
        file.write(eval(response))
        file.close()
        return True
    except Exception as e:
        print(e)
        print('File not downloaded')
        return False

def send_file_to_server(connection, file_path):
    try:
        file = open(file_path, 'rb')
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_data = file.read(file_size)
        connection.send(to_request('upload-file', {
            'bytes' : file_data,
            'name' : file_name,
            'size': file_size
            }))

        file.close()
        return True
    except Exception as e:
        print(e)
        return False



