import pickle
import os

def load_account():
    try:
        with open('./server/assets/documents/accounts.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(e)
        return {}


def save_account(account):
    try:
        accounts = load_account()
        accounts.update(account)
        with open('./server/assets/documents/accounts.pkl', 'wb') as f:
            pickle.dump(account, f)
    except Exception as e:
        print(e)
        return False
    return True

def all_files():
    return os.listdir('./server/assets/data')


def create_file(name, bytes):
    try:
        with open('./server/assets/data/' + name, 'wb') as f:
            f.write(bytes)
    except Exception as e:
        print(e)
        return False
    return True

def get_file_bytes(name):
    file_bytes = b""
    try:
        with open('./server/assets/data/' + name, 'rb') as f:
            file_bytes = f.read()
    except Exception as e:
        print(e)
        return False
    return file_bytes

