import sqlite3
from datetime import datetime

# database name : comp-info.sqlite, contains 4 tables
# Tables : IPees, Computers, Users, Info
# IPees fields : IP, Status(up\down)
# Computers fields : Bios serial number, Computer Name. Both fields are Unique
# Users fields : Users, domain
# Info fields : Computer Name, Username, IP, Status


def db_init():
    conn = sqlite3.connect('./HelpSelf/comp-info.sqlite3')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS IPees
    (Id INTEGER NOT NULL, IP Text, Status INTEGER, UNIQUE(Id,IP), PRIMARY KEY("Id" AUTOINCREMENT))''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Computers
    (Id INTEGER NOT NULL, BIOS_Serial TEXT, Comp_Name TEXT, UNIQUE(Id,BIOS_Serial,Comp_Name), 
    PRIMARY KEY("Id" AUTOINCREMENT))''')
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
    (Id INTEGER NOT NULL UNIQUE, Comp_Track INTEGER, User_Track INTEGER, IP_Track INTEGER, Status_Track INTEGER, 
    Logged_On_Track TEXT,
    PRIMARY KEY("Id" AUTOINCREMENT), 
    FOREIGN KEY("Comp_Track") REFERENCES Computers (Id) ON DELETE CASCADE, 
    FOREIGN KEY("User_Track") REFERENCES Users (Id), 
    FOREIGN KEY("IP_Track") REFERENCES IPees (Id), 
    FOREIGN KEY("Status_Track") REFERENCES IPees (Id))''')
    conn.close()


def db_conn():
    conn_db = sqlite3.connect('comp-info.sqlite')
    curse = conn_db.cursor()
    return curse, conn_db


def db_close_conn(conn_db):
    conn_db.close()

    #


def checkdb(received_name):
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # checking whether the computer is already registered
    namecheck = ''
    existence_status = 0
    try:
        curse.execute("SELECT Comp_Name FROM Computers WHERE Comp_Name = ?", (received_name,))
        row = curse.fetchone()
        namecheck = row[0]
        if received_name == namecheck:
            existence_status = 1
    except:
        existence_status = 0
    # Closing Connection to DataBase
    db_close_conn(conn_db)
    return existence_status

    #


def db_insert(client_instance):
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # not registered before 2
    #   inserting data
    curse.execute(''' INSERT INTO Computers(BIOS_Serial,Comp_Name) VALUES(?,?) ''',
                  (client_instance.biosserial, client_instance.computername))
    conn_db.commit()
    comp_id = curse.lastrowid
    curse.execute(''' INSERT INTO Users(User,Domain) VALUES(?,?) ''',
                  (client_instance.username, client_instance.domain))
    conn_db.commit()
    user_id = curse.lastrowid
    curse.execute(''' INSERT INTO IPees(IP,Status) VALUES(?,?) ''', (client_instance.address, client_instance.status))
    conn_db.commit()
    ip_id = curse.lastrowid
    updated_on = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    curse.execute(''' INSERT INTO Info(Comp_Id,User_Id,IP_Id,Status_Id, Logged_On) VALUES(?,?,?,?,?) ''',
                  (comp_id, user_id, ip_id, ip_id, updated_on))
    conn_db.commit()
    curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Status_Track,Logged_On_Track) 
    VALUES(?,?,?,?,?) ''', (comp_id, user_id, ip_id, ip_id, updated_on))
    conn_db.commit()
    print(f"user id {user_id}")
    # Closing Connection to DataBase
    db_close_conn(conn_db)


def db_search(to_be_searched, choice):
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # checking whether the computer is already registered
    check = ''
    checkl = ''
    found = 0
    try:
        if choice == 1:
            curse.execute('''SELECT Id, Comp_Name FROM Computers WHERE BIOS_Serial = ?''', (to_be_searched,))
        elif choice == 2:
            curse.execute('''SELECT Id, Status FROM IPees WHERE IP = ?''', (to_be_searched,))
        elif choice == 3:
            curse.execute('''SELECT Id, Domain FROM Users WHERE User = ?''', (to_be_searched,))
        elif choice == 4:
            curse.execute('''SELECT Id, Logged_On FROM Info WHERE Comp_Id = ?''', (to_be_searched,))
        row = curse.fetchone()
        check = row[0]
        checkl = row[1]
        found = 1
    except:
        found = 0
    # Closing Connection to DataBase
    db_close_conn(conn_db)
    return found, check, checkl


def db_update(client_instance):
    # Connecting to DataBase
    curse, conn_db = db_conn()

    f1, c1, cl = db_search(client_instance.biosserial, 1)
    print(f"c1 : {c1} {type(c1)}, bios {client_instance.biosserial} {type(client_instance.biosserial)}")
    if len(str(cl)) < 1:
        curse.execute(''' INSERT INTO Computers(BIOS_Serial,Comp_Name) VALUES(?,?) ''',
                      (client_instance.biosserial, client_instance.computername))
        conn_db.commit()
        c1 = curse.lastrowid

    f2, c2, cl = db_search(client_instance.address, 2)
    if len(str(cl)) >= 1:
        curse.execute('''Update IPees set Status = 1 where id = ?''', (c2,))
    else:
        curse.execute(''' INSERT INTO IPees(IP,Status) VALUES(?,?) ''',
                      (client_instance.address, client_instance.status))
        conn_db.commit()
        c2 = curse.lastrowid

    f3, c3, cl = db_search(client_instance.username, 3)
    if len(str(cl)) < 1:
        curse.execute(''' INSERT INTO Users(User,Domain) VALUES(?,?) ''',
                      (client_instance.username, client_instance.domain))
        conn_db.commit()
        c3 = curse.lastrowid
    updated_on = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f4, c4, cl = db_search(c1, 4)
    if len(str(cl)) >= 1:
        curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Status_Track,Logged_On_Track) 
        VALUES(?,?,?,?,?) ''', (c1, c3, c2, c2, updated_on))
        conn_db.commit()
        curse.execute('''Update Info set Comp_Id = ?, User_Id = ?, IP_Id = ?, Status_Id = ? , Logged_On = ? 
        where id = ?''', (c1, c3, c2, c2, updated_on, c4))
        conn_db.commit()
    else:
        curse.execute(''' INSERT INTO Track(Comp_Track,User_Track,IP_Track,Status_Track,Logged_On_Track) 
        VALUES(?,?,?,?,?) ''', (c1, c3, c2, c2, updated_on))
        conn_db.commit()
        curse.execute(''' INSERT INTO Info(Comp_Id,User_Id,IP_Id,Status_Id,Logged_On) VALUES(?,?,?,?,?) ''',
                      (c1, c3, c2, c2, updated_on))
        conn_db.commit()
        info_id = curse.lastrowid

    # Closing Connection to DataBase
    db_close_conn(conn_db)
