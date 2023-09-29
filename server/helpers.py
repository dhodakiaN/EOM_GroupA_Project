import pickle  # For serializing and deserializing Python object structures
import os  # For interacting with the operating system


def load_account():
    """
    Loads and returns the accounts from a pickle file.

    :return: A dictionary containing account information, or an empty dictionary if an error occurs.
    """
    try:
        # Opening the accounts.pkl file in binary read mode
        with open('./server/assets/documents/accounts.pkl', 'rb') as f:
            # Loading and returning the accounts dictionary from the file
            return pickle.load(f)
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        return {}  # Returning an empty dictionary in case of an error


def save_account(account):
    """
    Updates and saves the given account information to a pickle file.

    :param account: A dictionary containing the account information to be saved.
    :return: True if the account is saved successfully, False otherwise.
    """
    try:
        accounts = load_account()  # Loading existing accounts
        # Updating the accounts dictionary with the given account information
        accounts.update(account)
        # Opening the accounts.pkl file in binary write mode
        with open('./server/assets/documents/accounts.pkl', 'wb') as f:
            # Dumping the updated account information to the file
            pickle.dump(account, f)
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        return False  # Returning False in case of an error
    return True  # Returning True if the account is saved successfully


def all_files():
    """
    Lists and returns all files in the specified data directory.

    :return: A list of file names in the specified data directory.
    """
    return os.listdir('./server/assets/data')  # Listing and returning all files in the specified directory


def create_file(name, bytes):
    """
    Creates a file with the given name and writes the given bytes to it.

    :param name: The name of the file to be created.
    :param bytes: The bytes to be written to the file.
    :return: True if the file is created successfully, False otherwise.
    """
    try:
        # Opening/Creating the file in binary write mode
        with open('./server/assets/data/' + name, 'wb') as f:
            f.write(bytes)  # Writing the given bytes to the file
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        return False  # Returning False in case of an error
    return True  # Returning True if the file is created successfully


def get_file_bytes(name):
    """
    Reads and returns the bytes of the file with the given name.

    :param name: The name of the file to be read.
    :return: The bytes of the file, or False if an error occurs.
    """
    file_bytes = b""  # Initializing an empty bytes object
    try:
        # Opening the file in binary read mode
        with open('./server/assets/data/' + name, 'rb') as f:
            file_bytes = f.read()  # Reading and storing the bytes of the file
    except Exception as e:  # Handling any exceptions that occur
        print(e)  # Printing the exception to the console
        return False  # Returning False in case of an error
    return file_bytes  # Returning the bytes of the file
