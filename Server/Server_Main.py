import socket
import time
import threading
from db_init_connection import db_init, db_insert, db_update, checkdb
from Client_Class import Info
from Sender_Receiver import send, receive_info, receive_name
HEADER = 64
PORT = 8888
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
EOF_MESSAGE = "!Name Sent"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # receiving computer name
    received_name = receive_name(conn)
    print(f"[{addr}] {received_name}")
    # checking the db whether the computer name exists
    existence_status = checkdb(received_name)
    # Sending existence status 1\2
    send(conn, str(existence_status))
    send(conn, EOF_MESSAGE)
    # receiving the list of data
    received_data = receive_info(conn)
    # printing for test sk,
    print(received_data)
    # Instantiating the class now for test reasons
    client_instance = Info(received_name)
    if existence_status == 1:
        # Call fun to obj
        client_instance.setinfo1(received_data)
        # Updating data
        db_update(client_instance)
        # printing for test sk,
        print('status 1')

    elif existence_status == 2:
        # Call fun to obj + bios serial
        client_instance.setinfo1(received_data)
        client_instance.setinfo2(received_data[4])
        # Inserting data
        db_insert(client_instance)
        # printing for test sk,
        print('status 2')

    conn.close()


def start():
    # Creating Database and its Tables
    db_init()
    time.sleep(2)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
