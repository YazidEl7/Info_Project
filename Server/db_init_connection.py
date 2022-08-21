import sqlite3
from datetime import datetime
import locale

# database name : comp-info.sqlite, contains 5 tables
# Tables : IPees, Computers, Users, Info, Track
# IPees fields : IP, Status(up\down)
# Computers fields : Bios serial number, Computer Name, Last_TimeCreated, CsvLog, system, release, version, machine.
# Users fields : Users, domain
# Info fields : Computer Name, Username, IP, Status, Logged_On
# Track fields : Computer Name, Username, IP, Logged_On
Date_Format = locale.getdefaultlocale()[0]


def to_fr_datetime():
    """ if Date_Format != 'fr_FR':
        updatedon = datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%m/%d/%Y %I:%M:%S %p").strftime(
            "%d/%m/%Y %H:%M:%S")
    else:
        updatedon = datetime.now().strftime("%d/%m/%Y %H:%M:%S")"""
    updatedon = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return updatedon


def db_init():
    conn = sqlite3.connect('./HelpSelf/comp-info.sqlite3')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS IPees
    (Id INTEGER NOT NULL, IP Text, Status INTEGER, UNIQUE(Id,IP), PRIMARY KEY("Id" AUTOINCREMENT))''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Computers
    (Id INTEGER NOT NULL, BIOS_Serial TEXT, Comp_Name TEXT, Last_TimeCreated TEXT, Csv_Log BLOB, System TEXT, 
    Release TEXT, Version TEXT, Machine TEXT, UNIQUE(Id,BIOS_Serial), PRIMARY KEY("Id" AUTOINCREMENT))''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users
    (Id INTEGER NOT NULL UNIQUE, User TEXT, Domain TEXT, PRIMARY KEY("Id" AUTOINCREMENT))''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Info
    (Id INTEGER NOT NULL UNIQUE, Comp_Id INTEGER UNIQUE, User_Id INTEGER, IP_Id INTEGER, Status_Id INTEGER, 
    Logged_On TEXT,
    PRIMARY KEY("Id" AUTOINCREMENT), 
    FOREIGN KEY("Comp_Id") REFERENCES Computers (Id) ON DELETE CASCADE, 
    FOREIGN KEY("User_Id") REFERENCES Users (Id), 
    FOREIGN KEY("IP_Id") REFERENCES IPees (Id), 
    FOREIGN KEY("Status_Id") REFERENCES IPees (Id))''')
    # ON delete
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Track
    (Id INTEGER NOT NULL UNIQUE, Comp_Track INTEGER, User_Track INTEGER, IP_Track INTEGER, Logged_On_Track TEXT,
    PRIMARY KEY("Id" AUTOINCREMENT), 
    FOREIGN KEY("Comp_Track") REFERENCES Computers (Id) ON DELETE CASCADE, 
    FOREIGN KEY("User_Track") REFERENCES Users (Id), 
    FOREIGN KEY("IP_Track") REFERENCES IPees (Id))''')
    conn.close()


def db_conn():
    conn_db = sqlite3.connect('./HelpSelf/comp-info.sqlite3')
    curse = conn_db.cursor()
    return curse, conn_db


def db_close_conn(conn_db):
    conn_db.close()

    #


def convert_to_binary(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def checkdb(received_biosserial):
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # checking whether the computer is already registered
    namecheck = ''
    idcheck = ''
    ltc = ''
    existence_status = 0
    try:
        curse.execute("SELECT Id, Comp_Name, Last_TimeCreated FROM Computers WHERE BIOS_Serial = ?",
                      (received_biosserial,))
        row = curse.fetchone()
        if row is not None:
            idcheck = row[0]
            namecheck = row[1]
            ltc = row[2]
            existence_status = 1
    except:
        existence_status = 0
    # Closing Connection to DataBase
    db_close_conn(conn_db)
    return existence_status, idcheck, namecheck, ltc

    #


def db_update_status():
    # Connecting to DataBase
    curse, conn_db = db_conn()
    curse.execute('''Update IPees set Status = 0''')
    conn_db.commit()
    # Closing Connection to DataBase
    db_close_conn(conn_db)


def db_insert(client_instance, received_ltc, directory, os):
    path = directory + "/LOGS/" + client_instance.biosserial + ".csv"
    b_data = convert_to_binary(path)
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # not registered before 2
    #   inserting data
    curse.execute(''' INSERT INTO Computers(BIOS_Serial,Comp_Name,Last_TimeCreated,Csv_Log,System,Release,
    Version,Machine) VALUES(?,?,?,?,?,?,?,?) ''', (client_instance.biosserial, client_instance.computername,
                                                   received_ltc, b_data, os[0], os[2], os[3], os[4]))
    conn_db.commit()
    comp_id = curse.lastrowid
    curse.execute(''' INSERT INTO Users(User,Domain) VALUES(?,?) ''',
                  (client_instance.username, client_instance.domain))
    conn_db.commit()
    user_id = curse.lastrowid
    curse.execute(''' INSERT INTO IPees(IP,Status) VALUES(?,?) ''', (client_instance.address, client_instance.status))
    conn_db.commit()
    ip_id = curse.lastrowid
    updated_on = to_fr_datetime()

    curse.execute(''' INSERT INTO Info(Comp_Id,User_Id,IP_Id,Status_Id, Logged_On) VALUES(?,?,?,?,?) ''',
                  (comp_id, user_id, ip_id, ip_id, updated_on))
    conn_db.commit()
    curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Logged_On_Track) 
    VALUES(?,?,?,?) ''', (comp_id, user_id, ip_id, updated_on))
    conn_db.commit()
    # Closing Connection to DataBase
    db_close_conn(conn_db)
    print(f"user id {user_id}")


def db_search(to_be_searched, choice):
    # checking whether the computer is already registered
    check = ''
    checkl = ''
    found = 0
    # Connecting to DataBase
    curse, conn_db = db_conn()
    try:
        # if choice == 1:
        # curse.execute('''SELECT Id, Comp_Name FROM Computers WHERE BIOS_Serial = ?''', (to_be_searched,))
        if choice == 2:
            curse.execute('''SELECT Id, Status FROM IPees WHERE IP = ?''', (to_be_searched,))
        elif choice == 3:
            curse.execute('''SELECT Id, Domain FROM Users WHERE User = ?''', (to_be_searched,))
        elif choice == 4:
            curse.execute('''SELECT Id, Logged_On FROM Info WHERE Comp_Id = ?''', (to_be_searched,))
        row = curse.fetchone()
        if row is not None:
            check = row[0]
            checkl = row[1]
            found = 1
    except:
        found = 0
    # Closing Connection to DataBase
    db_close_conn(conn_db)
    return found, check, checkl


def db_update(client_instance, c1, cl, received_ltc, directory, appended, os_r, os):

    path = directory + "/LOGS/" + client_instance.biosserial + ".csv"
    b_data = convert_to_binary(path)
    # Connecting to DataBase
    curse, conn_db = db_conn()

    curse.execute('''UPDATE Computers SET Last_TimeCreated = ? WHERE Id = ?''', (received_ltc, c1))
    conn_db.commit()

    if appended == 1:
        curse.execute('''UPDATE Computers SET Csv_Log = ? WHERE Id = ?''', (b_data, c1))
        conn_db.commit()

    if os_r == 1:
        curse.execute('''UPDATE Computers SET System = ?, Release = ?, Version = ?, Machine = ? WHERE Id = ?''',
                      (os[0], os[2], os[3], os[4], c1))
        conn_db.commit()

    # print(f"c1 : {c1} {type(c1)}, bios {client_instance.biosserial} {type(client_instance.biosserial)}")
    if cl != client_instance.computername:
        # print(f"this is cl {cl} {type(cl)} this is coming {client_instance.computername} c1 {c1} {type(c1)}")
        curse.execute('''UPDATE Computers SET Comp_Name = ? WHERE Id = ?''', (client_instance.computername, c1))
        conn_db.commit()

    f2, c2, cl = db_search(client_instance.address, 2)
    if f2 == 1:
        curse.execute('''UPDATE IPees SET Status = 1 WHERE Id = ?''', (c2,))
        conn_db.commit()
    else:
        curse.execute(''' INSERT INTO IPees(IP,Status) VALUES(?,?) ''',
                      (client_instance.address, client_instance.status))
        conn_db.commit()
        c2 = curse.lastrowid

    f3, c3, cl = db_search(client_instance.username, 3)
    if f3 != 1 or cl != client_instance.domain:
        curse.execute(''' INSERT INTO Users(User,Domain) VALUES(?,?) ''',
                      (client_instance.username, client_instance.domain))
        conn_db.commit()
        c3 = curse.lastrowid
    updated_on = to_fr_datetime()

    f4, c4, cl = db_search(c1, 4)
    if f4 == 1:
        curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Logged_On_Track) 
        VALUES(?,?,?,?,?) ''', (c1, c3, c2, updated_on))
        conn_db.commit()
        curse.execute('''Update Info SET Comp_Id = ?, User_Id = ?, IP_Id = ?, Status_Id = ? , Logged_On = ? 
        WHERE id = ?''', (c1, c3, c2, c2, updated_on, c4))
        conn_db.commit()
    else:
        curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Logged_On_Track) 
        VALUES(?,?,?,?,?) ''', (c1, c3, c2, updated_on))
        conn_db.commit()
        curse.execute(''' INSERT INTO Info(Comp_Id,User_Id,IP_Id,Status_Id,Logged_On) VALUES(?,?,?,?,?) ''',
                      (c1, c3, c2, c2, updated_on))
        conn_db.commit()
        info_id = curse.lastrowid

    # Closing Connection to DataBase
    db_close_conn(conn_db)
