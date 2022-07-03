import socket
import threading
from db_init_connection import db_init, db_conn, db_close_conn

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

    def send(conn, mesg):
        state = mesg.encode(FORMAT)
        state_length = len(state)
        send_length = str(state_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(state)

    #

    def receive_name(conn):
        msgg = ''
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                msgg += msg
                if msg == EOF_MESSAGE:
                    msgg = msgg.replace(EOF_MESSAGE, '')
                    connected = False
        return msgg

    #
    def receive_info(conn):
        msgg = ''
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                msgg += msg
                if msg == EOF_MESSAGE:
                    msgg = eval(msgg.replace(EOF_MESSAGE, ''))
                    connected = False
        return msgg

    #
    def checkdb(cur, received_name):
        # checking whether the computer is already registered
        namecheck = ''
        existence_status = 2
        try:
            cur.execute("SELECT Comp_Name FROM Computers WHERE Comp_Name = ?", (received_name,))
            row = cur.fetchone()
            namecheck = row[0]
            if received_name == namecheck:
                existence_status = 1
        except:
            existence_status = 2
        return existence_status

    #
    # receiving computer name
    received_name = receive_name(conn)
    print(f"[{addr}] {received_name}")
    # Connecting to DataBase
    cur, con_n = db_conn()
    # checking the db whether the computer name exists
    existence_status = checkdb(cur, received_name)
    # Sending existence status 1\2
    send(conn, str(existence_status))
    send(conn, EOF_MESSAGE)
    # receiving the list of data
    received_data = receive_info(conn)
    # printing for test sk,
    print(received_data)
    if existence_status == 1:
        # Call fun to obj
        # printing for test sk,
        print('status 1')

    elif existence_status == 2:
        # Call fun to obj + bios serial
        # printing for test sk,
        print('status 2')

    # Closing Connection to DataBase
    db_close_conn(con_n)
    conn.close()


def start():
    # Creating Database and its Tables
    db_init()
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
