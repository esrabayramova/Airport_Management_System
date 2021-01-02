# Airport_Management_System
Flask Restful Api and Flask SQLAlchemy

## Description

This is an airport management system that is created by using Flask Restful API and Flask SQLAlchemy. There are two roles: admin and user. User can enter 2 parameters - city of departure and destination city. The, they will see the current flights between these two cities. Admin should login first by entering login_name and password. After signing in, admin can add, update, delete flights, see all flights and flights between two particular cities. After completing, admin ends the session.

## Installation

```
git clone https://github.com/esrabayramova/Airport_Management_System
```
## Usage

Firstly, one terminal is opened for server side. In this terminal, app.py file should be run, so that admins and users can use the system.
(!!!P.S. If the database is not created, in app.py file db.create_all() function must be run. In my case, I have created the database, so I commented it out.)


```
python3 app.py
```

Secondly, the file add_admin.py should be run, so that login_names and passwords of the administrators can be added to the database and they can access the system. (In my case, I have already run the file and added the admins to the database) Then, if you are a user, you can run user.py in another terminal. Here, you have to enter two parameters - city of departure and destination city. Then, you will see the list of the flights between these 2 cities (one-way).

```
python3 user.py
```

Then, if you want to use the system as an admin, you should run admin.py file in another terminal. First, you will have to enter login name and password. It authentication and authorization is successful, then you can enter one of the next parameters as an input: add, update, delete, get, get_all or end. If you enter end, the session will be terminated. Otherwise, you will be prompted to enter some necessary data in order to carry out the function add, get, delete and update.
```
python3 admin.py
```

After getting the necessary data, the user will be terminated automatically, but the admin has to end the session. You can terminate the server by entering ctrl+c in the terminal where app.py is running.
