import socket
import time
import threading
from db_init_connection import db_init, db_insert, db_update, checkdb
from Client_Class import Info
from Sender_Receiver import receive_info, receive_name
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

    # receiving the list of data
    received_data = receive_info(conn)
    # printing for test sk,
    print(f"Received data : {received_data}")
    # Instantiating the class now for test reasons
    client_instance = Info(received_name)
    client_instance.setinfo(received_data)
    if existence_status == 1:
        print(f"{received_name}")
        # Updating data
        db_update(client_instance)
        # printing for test sk,
        print('status 1 : computername exist')

    elif existence_status == 0:
        # Inserting data
        db_insert(client_instance)
        # printing for test sk,
        print('status 0 : computername doesnt exist')

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
    a, p = (str(SERVER), str(ADDR))
    create_service(a, p)
    # Start listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} : {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
