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
    con_n = sqlite3.connect('comp-info.sqlite')
    cur = con_n.cursor()
    return cur, con_n


def db_close_conn(con_n):
    con_n.close()

