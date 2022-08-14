import socket
import time
import os
import subprocess
import pandas
from dateutil import parser
import locale
import datetime


def info():
    #   Exist(1) send username, ip and status
    mylist = []
    username = {"username": os.getlogin().upper()}
    mylist.append(username)
    # systeminfo | findstr /B "Domain"
    # wmic computersystem get domain
    command = "echo %USERDOMAIN%"
    domain = {"domain": os.popen(command).read().replace('\n', '').upper()}
    # domain = {"domain": os.environ['userdomain'].upper()}
    mylist.append(domain)
    ip = {"IP": str(socket.gethostbyname(socket.gethostname()))}
    mylist.append(ip)
    #   Sending status 1 to update IP status to UP
    status = {"status": 1}
    mylist.append(status)
    command = "wmic bios get serialnumber"
    bios_ser = os.popen(command).read().replace("\n", "").replace("SerialNumber  ", "").replace("      ", "")
    bios_ser = {"bios_serial": bios_ser.upper()}
    mylist.append(bios_ser)
    return mylist


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def send_file(path):
    f_l = open(path, "r")
    line = f_l.readlines()
    f_l.close()
    j = 1
    while j < len(line):
        send(line[j])
        j = j + 1
    send(EOF_MESSAGE)


'''def receive():
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
    return state '''


def receive_tc():
    msgg = ''
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            msgg += msg
            if msg == EOF_MESSAGE:
                msgg = msgg.replace(EOF_MESSAGE, '')
                connected = False
    return msgg


def logfile(tc):
    log_cmd = 'Get-WinEvent -LogName "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational" ' \
              '-Oldest | Select-Object TimeCreated, Id, LevelDisplayName, Message, MachineName | ' \
              'Export-CSV -NoTypeInformation -Encoding UTF8 -Path "./computer_log.csv" -Delimiter ";"'
    subprocess.run(["powershell", "-Command", log_cmd], capture_output=True)
    if tc != 0:
        csv_file = pandas.read_csv('./computer_log.csv', delimiter=';')
        tc_0 = parser.parse(tc, dayfirst=True)
        i = 0
        log_text = '"TimeCreated";"Id";"LevelDisplayName";"Message";"MachineName"\n'
        while i < len(csv_file):
            c_tc = csv_file['TimeCreated'][i]
            if Date_Format == 'fr_FR':
                tc_1 = parser.parse(c_tc, dayfirst=True)
                fr_time = c_tc
            else:
                tc_1 = parser.parse(c_tc)
                fr_time = datetime.datetime.strptime(c_tc, "%m/%d/%Y %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")

            if tc_1 >= tc_0:
                log_text = log_text + fr_time + ';' + csv_file['Id'][i] + ';' + \
                           csv_file['LevelDisplayName'][i] + ';' + \
                           csv_file['Message'][i].replace('\r', '').replace('\n', ',') + ';' + \
                           csv_file['MachineName'][i] + '\n'
        if len(log_text) != 0:
            f_l = open("./filtered_log.csv", "w")
            f_l.write(log_text)
            f_l.close()
            send_file("./filtered_log.csv")
        else:
            send(EOF_MESSAGE)
    else:
        send_file("./computer_log.csv")


HEADER = 64
PORT = "yporty"
FORMAT = 'utf-8'
EOF_MESSAGE = "! Sent"
SERVER = "yaddry"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Connection_Status = 0
Date_Format = locale.getdefaultlocale()[0]
while True:
    while True:
        #   Already registered in database wait an hour to update server info
        if Connection_Status == 1:
            time.sleep(3600)
        #   Just logged in or not yet registered in database wait 3 minutes, we'll make it 3 seconds just for tests
        elif Connection_Status == 0:
            time.sleep(180)

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
            comp_name = os.environ['COMPUTERNAME']
            send(comp_name)
            #   After every sg we are required to send EOF_MESSAGE, so that server on receive could break out of loop
            send(EOF_MESSAGE)
            # the data we'll send is a list of dictionaries
            List_to_Send = []
            try:
                # Sending the List
                List_to_Send = info()
                send(str(List_to_Send))
                send(EOF_MESSAGE)
                # Receive NoNe or Last TimeCreated
                server_tc = receive_tc()
                # Send Last TimeCreated or Last TimeCreated to PC Last TimeCreated
                tc_cmd = '(Get-WinEvent -LogName "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational"' \
                         ' -MaxEvents 1).TimeCreated.ToString("dd/MM/yyyy hh:mm:ss")'
                completed = subprocess.run(["powershell", "-Command", tc_cmd], capture_output=True)
                send(completed.stdout.decode())
                send(EOF_MESSAGE)
                # we should add l8r something to control when we send the logs
                # Create logs file
                if server_tc == "NoNe":
                    logfile(0)
                else:
                    logfile(server_tc)
                # Send File
            except:
                # Failed sending
                Connection_Status = 0
                break
            # waiting for 60 seconds before closing,
            time.sleep(60)
            client.close()
