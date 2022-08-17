import socket
import time
import threading
from Server.db_init_connection import db_init, db_insert, db_update, checkdb, db_update_status
from Server.Client_Class import Info
from Server.Sender_Receiver import receive_info, receive, send, receive_file
import os
import sys
import PyInstaller.__main__
from datetime import datetime

HEADER = 64
PORT = 60006
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
EOF_MESSAGE = "! Sent"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # receiving computer name
    received_name = receive(conn)
    print(f"[{addr}] {received_name}")
    print(conn)
    # receiving the list of data
    received_data = receive_info(conn)
    # receiving OS info
    os_info = ''
    os_r = int(receive(conn))
    if os_r == 1:
        os_info = receive_info(conn)
    # printing for test sk,
    print(f"Received data : {received_data}")
    # Instantiating the class now for test reasons
    client_instance = Info(received_name)
    client_instance.setinfo(received_data)
    # checking the db whether the computer serial name exists
    existence_status, idcheck, namecheck, ltc = checkdb(client_instance.biosserial)
    directory = os.getcwd()

    received_ltc = ''
    appended = 0
    if existence_status == 1:
        print(f"{received_name}")
        # printing for test sk,
        print('status 1 : computer exist')
        log_r = int(receive(conn))
        if log_r == 1:
            # Send Last TimeCreated
            send(conn, ltc)
            send(conn, EOF_MESSAGE)
            # Receive Last TimeCreated
            received_ltc = receive(conn)
            # Receive file and append to it
            appended = receive_file(conn, directory, client_instance.biosserial)
        # Updating data
        db_update(client_instance, idcheck, namecheck, received_ltc, directory, appended, os_r, os_info)

    elif existence_status == 0:
        # printing for test sk,
        print('status 0 : computer doesnt exist')
        log_r = int(receive(conn))
        if log_r == 1:
            send(conn, "NoNe")
            send(conn, EOF_MESSAGE)
            # Receive Last TimeCreated
            received_ltc = receive(conn)
            # Create file with computerName
            log_file = open(f"{directory}/LOGS/{client_instance.biosserial}.csv", "w")
            log_headers = '"TimeCreated";"Id";"LevelDisplayName";"Message";"MachineName"\n'
            log_file.write(log_headers)
            log_file.close()
            # Receive file
            appended = receive_file(conn, directory, client_instance.biosserial)
        # Inserting data
        db_insert(client_instance, received_ltc, directory, os_info)

    conn.close()


def create_service(a, p):
    application_path = os.path.dirname(sys.executable)
    directory = os.getcwd()
    clt = open(f"{directory}/Client/Client_Service.txt", "r")
    clt_code = clt.read()
    clt.close()
    clt = open(f"{directory}/Client/Client_Service.py", "w")
    clt_code = clt_code.replace('"yporty"', p)
    clt_code = clt_code.replace('"yaddry"', a)
    clt.write(clt_code)
    clt.close()
    ''' 
    command = f'pyinstaller --noconfirm --onefile --windowed  "{application_path}/Client/Client_Service.py" ' \
              f'--distpath={application_path}/Client'
    c_s = os.popen(command) '''
    try:
        PyInstaller.__main__.run([
            'I:/52 weeks Py/Info_Project-main/Server/Caller.py',
            f'--distpath={directory}/Client',
            '--onefile',
            '--windowed',
            '--noconfirm'
        ])
    except:
        print("FAILED to Create Client .EXE Service")


def start():
    # Creating Database and its Tables
    db_init()
    time.sleep(2)
    # Creating client .exe service
    a = str(SERVER)
    p = str(ADDR)
    # create_service(a, p)
    # Start listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} : {ADDR}")

    # Experimental 1
    def check_st():
        threading.Timer(177.5, check_st).start()
        print('Updating IP status to down')
        db_update_status()

    # start_m = int(datetime.now().strftime("%M"))
    # start_d = int(datetime.now().strftime("%d"))
    check_st()
    while True:
        '''
        comp_m = int(datetime.now().strftime("%M"))
        comp_d = int(datetime.now().strftime("%d"))
        if comp_m >= (start_m + 3) or comp_d > start_d:
            start_m = int(datetime.now().strftime("%M"))
            db_update_status()
        # elif comp_m < (start_m+3):
        '''
        print('waiting for new connection to accept')
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    # End Experimental 1


print("[STARTING] server is starting...")
start()
