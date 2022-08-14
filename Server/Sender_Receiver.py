
HEADER = 64
FORMAT = 'utf-8'
EOF_MESSAGE = "! Sent"


def send(conn, mesg):
    state = mesg.encode(FORMAT)
    state_length = len(state)
    send_length = str(state_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(state)


#

def receive(conn):
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


def receive_file(conn, directory, serial):
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
    if len(msgg) != 0:
        log_file = open(f"{directory}/LOGS/{serial}.csv", "a")
        log_file.write(msgg)
        log_file.close()
        return 1
    else:
        return 0


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
