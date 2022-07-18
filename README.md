# Info_Project
The purpose of this little project is to help you when a user calls you about a problem in his computer by providing you with the necessary informtion to connect remotely
Also to limit remote access to servers that might give you informations about a computer.

This project consists of two parts; the main idea is that the 1st part contains a server that receives data from clients and it stores it in a database, 
the 2nd part contains a Django app that’ll access that database and get data in order to show it in tables.

## 1st part: 

```mermaid
graph TD;
    /Info_Project-->/Server_Main.py;
    /Info_Project-->/Server;
    /Info_Project-->/Client;
    /Client-->/Client_Service.py;
    /Server-->/Client_Class.py;
    /Server-->/db_init_connection.py;
    /Server-->/Sender_Receiver.py;
    /Info_Project-->/HelpSelf;
    /HelpSelf-->/comp-info.sqlite3;
```
 
![comp-info](/assets/images/comp-info.jpg)

```mermaid
graph TD;
    A[ComputerName] --> B{Exist in DB?};
    B -->|Yes| C[Update];
    C --> D{serial in Info is the serial received?};
    D --> |No| F[Insert the name in Computers];
    C --> G{Received IP exist?};
    G --> |No| H[Insert the IP in IPees];
    G --> |Yes| I[Insert the IP in IPees];
    C --> J{Received User exist?};
    J --> |No| K[Insert the user in Users];
    C --> L{Computer exist in Info?};
    L --> |Yes| M[Update Info & Insert Into Track];
    L --> |No| N[Insert into Info & Track];
    B ---->|No| E[Insert in Info & Track];
```

## 2nd part: 

```mermaid
graph TD;
    /Info_Project-->/HelpSelf;
    /HelpSelf-->/comp-info.sqlite3;
    /HelpSelf-->/HelpInfo;
    /HelpInfo-->/static;
    /static-->/Dynamic;
    /Dynamic-->/logged_users.json;
    /static-->/HelpInfo/main.css;
    /HelpInfo-->/templates/HelpInfo;
    /templates/HelpInfo-->/index.html;
    /templates/HelpInfo-->/data.html;
    /templates/HelpInfo-->/logs.html;
    /templates/HelpInfo-->/users_history.html;
    /templates/HelpInfo-->/registration;
    /registration-->login.html;
```
### logged Users :

At successful login we gonna take the HTTP headers and store what we want in a JSON file, 
in order to make a table of users that logged plus a few other details.

![logged-users](/assets/images/logged_users.jpg)

![login-page](/assets/images/login.jpg)
### Home page:
Contains current users on each computer.<br/>
Notice : when you click on a row it shows you every user that has logged in to that computer !

![computers](/assets/images/COMPUTERS.jpg)

### logged on users logs

![logs](/assets/images/LOGS.jpg)

### Users History:
it keeps track of every computer a user has logged on to and when was that exactly.<br/>
Notice : when you click on a row it shows you every computer that that user has logged on to before !

![Users-History](/assets/images/USERS_HISTORY.jpg)
