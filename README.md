# Info_Project
The purpose of this little project is to help you when a user calls you about a problem in his computer by providing you with the necessary information to connect remotely.
Also to limit remote access to servers that might give you informations about a computer.

This project consists of two parts; the main idea is that the 1st part contains a server that receives data from clients and it stores it in a database, 
the 2nd part contains a Django app that’ll access that database and get data in order to show it in tables.

**Might work on the below stuff l8r** : 
- Still needs to be tested in restricting Environments (I tested it in a windows 10 PC with a standard user and it worked, but l8r when we pull logs too we'll have to test it again)
- Perhaps We get more data, like OS version ...
- Needs a function on Server_Main that'll change Status to 0, after 3min without a syn with a specific computer.
- Before utilization, change IP adress on client, port number if you want and create your own admin user on Django.
- changing the status field on the website to show colored indicators.
- Make the client service run silently.

## 1st part: 

**Server_Main.py** : Launch it on server <br/>
**Client_Service** : Launch it on client side, but change the server adress that it'll connect to, according to yours.

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

**db_init_connection.py** : A bit of what happens.
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

**Views** : between is the view I implemented for upon log in logging.

```mermaid
graph TD;
    A[http://127.0.0.1] --> B[views : m];
    B --> C{is the User authenticated?};
    C --> |Yes| D[redirect_to : /Home, views : data];
    C --> |No| E[redirect_to : /login/ ];
    E --> F{authentication succeded?};
    F --> |Yes| G[redirect_to : /between --for logging--, views : between];
    G --> H[redirect_to : /Home, views : data];
```

![login-page](/assets/images/login.jpg)

### Home page:
Contains current users on each computer.<br/>
**Notice** : when you click on a row it shows you every user that has logged in to that computer !

![computers](/assets/images/COMPUTERS.jpg)

### logged on users logs

![logs](/assets/images/LOGS.jpg)

### Users History:
it keeps track of every computer a user has logged on to and when was that exactly.<br/>
**Notice** : when you click on a row it shows you every computer that that user has logged on to before !

![Users-History](/assets/images/USERS_HISTORY.jpg)
