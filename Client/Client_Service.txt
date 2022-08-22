import socket
import time
import os
import subprocess
import pandas
from dateutil import parser
import locale
import datetime
import platform

HEADER = 64
PORT = "yporty"
FORMAT = 'utf-8'
EOF_MESSAGE = "! Sent"
SERVER = "yaddry"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Connection_Status = 0
Date_Format = locale.getdefaultlocale()[0]
OTS = 1
RS = 1


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
                fr_time = datetime.datetime.strptime(c_tc, "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")

            if tc_1 >= tc_0:
                log_text = log_text + fr_time + ';' + str(csv_file['Id'][i]) + ';' + \
                           csv_file['LevelDisplayName'][i] + ';' + \
                           csv_file['Message'][i].replace('\r', '').replace('\n', ',') + ';' + \
                           csv_file['MachineName'][i] + '\n'
            i = i + 1
        if len(log_text) != 0:
            f_l = open("./filtered_log.csv", "w")
            f_l.write(log_text)
            f_l.close()
            send_file("./filtered_log.csv")
        else:
            send(EOF_MESSAGE)
    else:
        csv_file = pandas.read_csv('./computer_log.csv', delimiter=';')
        i = 0
        log_text0 = '"TimeCreated";"Id";"LevelDisplayName";"Message";"MachineName"\n'
        while i < len(csv_file):
            timec = csv_file['TimeCreated'][i]
            if Date_Format != 'fr_FR':
                timec = datetime.datetime.strptime(timec, "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %H:%M:%S")
            log_text0 = log_text0 + timec + ';' + str(csv_file['Id'][i]) + ';' + csv_file['LevelDisplayName'][i] + ';' + \
                        csv_file['Message'][i].replace('\r', '').replace('\n', ',') + ';' + \
                        csv_file['MachineName'][i] + '\n'
            i = i + 1
        if len(log_text0) != 0:
            f_l = open("./computer_log.csv", "w")
            f_l.write(log_text0)
            f_l.close()
        send_file("./computer_log.csv")


def hour_plus_one():
    v = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')
    vv = v[1].split(':')
    c = int(vv[0])
    if c == 22:
        vv = "00" + ":" + vv[1] + ":" + vv[2]
    elif c==23:
        vv = "01" + ":" + vv[1] + ":" + vv[2]
    else:
        vv = str(int(vv[0]) + 2) + ":" + vv[1] + ":" + vv[2]
    v = v[0] + " " + vv
    if Date_Format == 'fr_FR':
        co = parser.parse(v, dayfirst=True)
    else:
        co = parser.parse(v)
    return co


##########################################################################################################
c = hour_plus_one()
while True:
    while True:
        if Date_Format == 'fr_FR':
            now = parser.parse(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), dayfirst=True)
        else:
            now = parser.parse(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        #####################################################################
        #   Already registered in database wait 3.5 minutes to update server info
        if Connection_Status == 1:
            time.sleep(210)
        #   Just logged in or not yet registered in database wait 2.5 minutes
        elif Connection_Status == 0:
            time.sleep(150)
        #####################################################################
        try:
            client.connect(ADDR)
            Connection_Status = 1
        except:
            # didn't connect
            Connection_Status = 0
        #####################################################################
        if Connection_Status == 0:
            break
        elif Connection_Status == 1:
            ###########################################################
            #   First we send computer name for db registration check
            comp_name = os.environ['COMPUTERNAME']
            send(comp_name)
            #   After every sg we are required to send EOF_MESSAGE, so that server on receive could break out of loop
            send(EOF_MESSAGE)
            ###########################################################
            # the data we'll send is a list of dictionaries
            List_to_Send = []
            try:
                # Sending the List
                List_to_Send = info()
                send(str(List_to_Send))
                send(EOF_MESSAGE)
                ###########################################################
                # sending OS info
                if OTS == 1:
                    send("1")
                    send(EOF_MESSAGE)
                    send(str(list(platform.uname())))
                    send(EOF_MESSAGE)
                    OTS = 0
                else:
                    send("0")
                ###########################################################
                if RS == 1 or now > c:
                    send("1")
                    send(EOF_MESSAGE)
                    # Receive NoNe or Last TimeCreated
                    server_tc = receive_tc()
                    # Send Last TimeCreated or Last TimeCreated to PC Last TimeCreated
                    tc_cmd = '(Get-WinEvent -LogName "Microsoft-Windows-TerminalServices-LocalSessionManager' \
                             '/Operational" -MaxEvents 1).TimeCreated.ToString("dd/MM/yyyy hh:mm:ss") '
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
                    RS = 0
                    if now > c:
                        c = hour_plus_one()
                else:
                    send("0")
                    send(EOF_MESSAGE)
                ###########################################################
            except:
                # Failed sending
                Connection_Status = 0
                break
            ##############################################################
            # waiting for 60 seconds before closing,
            time.sleep(60)
            client.close()
#######################################################################################################
