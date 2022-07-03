
HEADER = 64
FORMAT = 'utf-8'
EOF_MESSAGE = "!Name Sent"


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
