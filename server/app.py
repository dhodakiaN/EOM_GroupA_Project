import socket  # For creating network connections
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For interacting with the operating system
from response import handle_requests  # For handling incoming requests


def runServer():
    """
    Initializes and runs the server, which listens for incoming connections and handles requests.
    """
    try:
        load_dotenv()  # Loading environment variables from a .env file
        # Creating a new socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = os.getenv('HOST')  # Getting the host from environment variables
        # Getting the port from environment variables and converting it to an integer
        port = int(os.getenv("PORT"))

        # Binding the server to the specified host and port
        server.bind((host, port))
        # Allowing the server to accept connections, with a backlog of 5
        server.listen(5)
        print("Server is running")  # Informing that the server is running
        while True:  # Main loop to keep the server running
            connection, _ = server.accept()  # Accepting an incoming connection
            # Receiving and decoding a request from the connection
            request = connection.recv(65536).decode('utf-8')

            if not request:  # If the request is empty, close the connection and continue
                connection.close()
                continue

            # Evaluating the request string to convert it to a Python object
            request = eval(request)
            event = request['event']  # Extracting the event from the request
            data = request['data']  # Extracting the data from the request

            print('event', event)  # Printing the event to the console
            print('data', data)  # Printing the data to the console

            # Handling the request based on the event and data
            handle_requests(event, connection, data)
            connection.close()  # Closing the connection after handling the request

    except Exception as e:  # Catching any exceptions that occur
        print(e)  # Printing the exception to the console
        # Informing that the server is not running
        print("Server is not running")


if __name__ == '__main__':
    # Checking if the script is being run as the main module,
    # and if so, calling the runServer function to start the server
    runServer()
