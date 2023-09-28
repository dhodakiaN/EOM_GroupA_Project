import os
import uuid
from time import sleep

def forced_input(message):
    while True:
        response = input(message)
        if response != "":
            return response


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def error_message(message):
    clear_screen()
    print(f'\n\033[1;31m{message}\033[0m\n')
    sleep(3)
    clear_screen()

def get_mac_address():
    """
    This function will return the mac address of this device
    """
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0, 8 * 6, 8)][::-1])


def to_request(event,data = {}):
    return str(
        {
            'event' : event,
            'data' : data
        }
    ).encode('utf-8')

