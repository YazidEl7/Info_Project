import sqlite3


# database name : comp-info.sqlite, contains 4 tables
# Tables : IPees, Computers, Users, Info
# IPees fields : IP, Status(up\down)
# Computers fields : Bios serial number, Computer Name. Both fields are Unique
# Users fields : Users, domain
# Info fields : Computer Name, Username, IP, Status


def db_init():
    conn = sqlite3.connect('comp-info.sqlite')
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
    PRIMARY KEY("Id" AUTOINCREMENT), 
    FOREIGN KEY("Comp_Id") REFERENCES Computers (Id), 
    FOREIGN KEY("User_Id") REFERENCES Users (Id), 
    FOREIGN KEY("IP_Id") REFERENCES IPees (Id), 
    FOREIGN KEY("Status_Id") REFERENCES IPees (Id))''')
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
    existence_status = 2
    try:
        curse.execute("SELECT Comp_Name FROM Computers WHERE Comp_Name = ?", (received_name,))
        row = curse.fetchone()
        namecheck = row[0]
        if received_name == namecheck:
            existence_status = 1
    except:
        existence_status = 2
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
    curse.execute(''' INSERT INTO IPees(IP,Status) VALUES(?,?) ''', (client_instance.adress, client_instance.status))
    conn_db.commit()
    ip_id = curse.lastrowid
    curse.execute(''' INSERT INTO Info(Comp_Id,User_Id,IP_Id,Status_Id) VALUES(?,?,?,?) ''',
                  (comp_id, user_id, ip_id, ip_id))
    conn_db.commit()
    # Closing Connection to DataBase
    db_close_conn(conn_db)


def db_update(client_instance):
    # Connecting to DataBase
    curse, conn_db = db_conn()
    # Updating data

    # Closing Connection to DataBase
    db_close_conn(conn_db)
