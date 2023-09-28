from helpers import load_account, save_account, all_files, create_file, get_file_bytes

def check_account(connection, data):
    try:
        accounts = load_account()
        mac_address = data['mac_address']
        if mac_address in accounts:
            connection.send(str(accounts[mac_address]).encode('utf-8'))
        else:
            raise Exception('Not authorized')
    except Exception as e:
        print(e)
        connection.send('not-authorized'.encode('utf-8'))


def create_account(connection, data):
    try:
        account = {
        data['mac_address'] : {
            'email' : data['email'],
            'username' : data['username']
        }
    }
        if save_account(account):
            connection.send('account-created'.encode('utf-8'))
        else:
            raise Exception('Account not created')
    except Exception as e:
        print(e)
        connection.send('account-not-created'.encode('utf-8'))

def get_files(connection):
    files = all_files()
    connection.send(str(files).encode('utf-8'))

def upload_file(connection, data):
    print('Trying to upload a file')
    try:
        print(data)
        if create_file(data['name'], data['bytes']):
            connection.send('file-uploaded'.encode('utf-8'))
        else:
            raise Exception('File not uploaded')
    except Exception as e:
        print(e)
        connection.send('file-not-uploaded'.encode('utf-8'))

def download_file(connection, data):
    try:
        file_bytes = get_file_bytes(data['name'])
        if file_bytes:
            connection.send(
                str(file_bytes).encode('utf-8')
            )
        else:
            raise Exception('File not found')
    except Exception as e:
        print(e)
        connection.send('file-not-found'.encode('utf-8'))
