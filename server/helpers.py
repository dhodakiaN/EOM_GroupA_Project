import pickle  # For serializing and deserializing Python object structures
import os  # For interacting with the operating system
import rsa # For public and private keys



def load_account():
    """
    Loads and returns the accounts from a pickle file.

    :return: A dictionary containing account information, or an empty dictionary if an error occurs.
    """
    try:
        # Opening the accounts.pkl file in binary read mode
        with open('server/assets/documents/accounts.pkl', 'rb') as f:
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
        with open('server/assets/documents/accounts.pkl', 'wb') as f:
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

def get_encryption_keys():
    """
    Reads directory in assets/keys and generates a 
    private or public key if it does not exist
    """ 

    # Define the directory for the keys
    keys_directory = "server/assets/keys/"

    # Check if the keys already exist
    public_key_path = os.path.join(keys_directory, "public.pem")
    private_key_path = os.path.join(keys_directory, "private.pem")

    if os.path.exists(public_key_path) and os.path.exists(private_key_path):
        print("Encryption keys already exist. Skipping key generation.")
        return

    # Create the directory if it doesn't exist
    if not os.path.exists(keys_directory):
        os.makedirs(keys_directory)

    # Generate new encryption keys
    public_key, private_key = rsa.newkeys(1024)

    # Save the public key
    with open(public_key_path, "wb") as f:
        f.write(public_key.save_pkcs1("PEM"))

    # Save the private key
    with open(private_key_path, "wb") as f:
        f.write(private_key.save_pkcs1("PEM"))

    print("Encryption keys generated and saved.")

def load_public_key():
    """
    This is to load the public key from file
    """
    keys_directory = "server/assets/keys/"
    public_key_path = os.path.join(keys_directory, "public.pem")
    
    if os.path.exists(public_key_path):
        with open(public_key_path, "rb") as f:
            public_key_data = f.read()
            public_key = rsa.PublicKey.load_pkcs1(public_key_data, format="PEM")
            return public_key
    else:
        return None
    
def load_private_key():
    keys_directory = "server/assets/keys/"
    private_key_path = os.path.join(keys_directory, "private.pem")
    
    if os.path.exists(private_key_path):
        with open(private_key_path, "rb") as f:
            private_key_data = f.read()
            private_key = rsa.PrivateKey.load_pkcs1(private_key_data, format="PEM")
            return private_key
    else:
        return None

def decrypt_data(encrypted_data, private_key):
    """
    Decrypt encrypted data using a private key.

    :param encrypted_data: The encrypted data to decrypt.
    :param private_key: The private key to use for decryption.
    :return: The decrypted data.
    """
    try:
        decrypted_data = rsa.decrypt(encrypted_data, private_key)
        return decrypted_data
    except rsa.pkcs1.DecryptionError as e:
        print("Decryption failed:", e)
        return None

