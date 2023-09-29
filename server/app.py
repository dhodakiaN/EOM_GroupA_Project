import socket
from dotenv import load_dotenv
import os
from response import handle_requests


def runServer():
    try:
        load_dotenv()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = os.getenv('HOST')
        port = int(os.getenv("PORT"))

        server.bind((host, port))
        server.listen(5)
        print("Server is running")
        while True:
            connection, _ = server.accept()
            # 2^16 = 65536
            request = connection.recv(65536).decode('utf-8')
            if not request:
                connection.close()
                continue
            request = eval(request)
            event = request['event']
            data = request['data']

            print('event', event)
            print('data', data)

            handle_requests(event, connection, data)
            connection.close()

    except Exception as e:
        print(e)
        print("Server is not running")



if __name__ == '__main__':
    runServer()
