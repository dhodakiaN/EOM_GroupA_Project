# Importing controller functions
from controllers import check_account, create_account, get_files, download_file, upload_file,request_public_key
from helpers import load_public_key

def handle_requests(event, connection, data=None):
    """
    Handles incoming requests based on the event type and sends responses back through the connection.

    :param event: A string representing the type of event or action to be performed.
    :param connection: The socket connection object through which responses are sent back.
    :param data: Optional. A dictionary containing any additional data needed for the request.
    """

    # Depending on the event type, the corresponding controller function is called with the appropriate parameters.
    if event == 'login':
        return check_account(connection, data)  # Handling login requests
    elif event == 'signup':
        # Handling account creation requests
        return create_account(connection, data)
    elif event == 'get-files':
        # Handling requests to get the list of files
        return get_files(connection)
    elif event == 'upload-file':
        print("uploading file")
        return upload_file(connection, data)  # Handling file upload requests
    elif event == 'download-file':
        # Handling file download requests
        return download_file(connection, data)
    elif event == 'Screenprint':
        connection.send("Data is printed on server side".encode('utf-8'))
    elif event == 'Screenprintenc':
        connection.send("Data is now encoded".encode('utf-8'))
    elif event == 'request-public-key':
        public_key = load_public_key()
        return request_public_key(connection, public_key)
    else:
        # Sending a response for invalid request types
        connection.send('invalid-request'.encode('utf-8'))
