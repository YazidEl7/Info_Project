import socket
import time
import os


def changeable_info():
    #   Exist(1) send username, ip and status
    mylist = []
    username = {"username": os.getlogin()}
    mylist.append(username)
    domain = {"domain": os.environ['userdomain']}
    mylist.append(domain)
    #   Sending status 1 to update IP status to UP
    status = {"status": 1}
    mylist.append(status)
    return mylist


def unchangeable_info(mylist):
    #   Doesn't exist (2) send the above plus bios serial
    command = "wmic bios get serialnumber"
    bios_ser = os.popen(command).read().replace("\n", "").replace("SerialNumber  ", "").replace("      ", "")
    bios_ser = {"bios_serial": bios_ser}
    mylist.append(bios_ser)
    return mylist


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive():
    state = ''
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            state += msg
            if msg == EOF_MESSAGE:
                #   changing state to int, because the only thing the server sends is an int
                state = int(state.replace(EOF_MESSAGE, ''))
                connected = False
    return state


HEADER = 64
PORT = 8888
FORMAT = 'utf-8'
EOF_MESSAGE = "!Name Sent"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Connection_Status = 0
while True:
    while True:
        #   Already registered in database wait an hour to update server info
        if Connection_Status == 1:
            time.sleep(3600)
        #   Just logged in or not yet registered in database wait 3 minutes, we'll make it 3 seconds just for tests
        elif Connection_Status == 0:
            time.sleep(3)

        try:
            client.connect(ADDR)
            Connection_Status = 1
        except:
            # didn't connect
            Connection_Status = 0

        if Connection_Status == 0:
            break
        elif Connection_Status == 1:
            #   First we send computer name for db registration check
            send(os.environ['COMPUTERNAME'])
            #   After every sg we are required to send EOF_MESSAGE, so that server on receive could break out of loop
            send(EOF_MESSAGE)
            #   next we wait to receive existence in db status, 1\2.
            Existence_Status = receive()
            # Next print is just for test sk, l8r we try to make the program run silently (In hidden window)
            print(Existence_Status)
            # the data we'll send is a list of dictionaries
            List_to_Send = []
            if Existence_Status == 1:
                #   Exist send username, ip and status
                List_to_Send = changeable_info()
            elif Existence_Status == 2:
                #   Doesn't exist send the above plus bios serial
                List_to_Send = changeable_info()
                List_to_Send = unchangeable_info(List_to_Send)
            else:
                # Failed receive break out of loop
                Connection_Status = 0
                break
            try:
                # Sending the List
                send(str(List_to_Send))
                send(EOF_MESSAGE)
            except:
                # Failed sending
                Connection_Status = 0
                break
            # waiting for 60 seconds before closing,
            time.sleep(60)
            client.close()

