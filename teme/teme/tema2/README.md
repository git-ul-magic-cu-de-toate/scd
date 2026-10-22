341C3 - Mihai Daniel Soare
Software Systems for Computer Networks

Homework 2 - REST Application using Flask & MySQL

December 2023

-------------


__Services__
------------

There are 3 available services in the `docker-compose.yml` file:

- `flask-app`
- `mysql-db`
- `adminer`

__`flask-app`__
- is an application using Flask Python module to create different HTTP routes available
for clients 

__Project structure:__


```
flask-app/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── setup.cfg
├── setup.py
├── src/
│   ├── database/
│   │   ├── constants.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── cities.py
│   │   ├── countries.py
│   │   ├── __init__.py
│   │   └── temperatures.py
│   ├── server.py
│   └── utils.py
└── startup.sh
```


- `Dockerfile` contains the rules needed to create a container with the application
- `startup.sh` is a file that runs when the container is created
- `setup.cfg` and `setup.py` are needed to install the application as a local module
for importing the files in the project when needed and not use a virtual
environment
- `src` is the main directory where the project is located
- `main.py` is the main file that starts the REST server
- `.dockerignore` contains `.pyc` objects and other useless stuff that shouldn't be copied
when running the container
- `requirements.txt` contains all the modules needed to be installed on the container


__``mysql-db``__

- a service that creates a mysql container from the latest mysql image
- has a volume for peristency
- is connected to the ``flask-app`` using a network
- is connected to the ``adminer`` using another network
- has named DNS by providing `container_name` rule in `docker-compose.yml` file
- has environment variables for creating the databases

__``adminer``__

- a service that creates an adminer container from the adminer image
- adminer is a pretty easy to use application to inspect databases

How to use the program
----------------------

__Commands__

- use the ``docker-compose up --build`` to build the 3 services available

__``adminer``__

- type `http://localhost:8080/` in browser and connect to the database using the credentials from the `docker-compose.yml` file

__``flask-app``__

- to test the application use postman locally

Design
------

__``flask-app``__

- `src/routes/` directory contains routes about:
    - cities
    - countries
    - temperatures

- `src/database/` directory contains:
    - `constants` which are queries for different mysql operations
    - `database` a `DatabaseDriver` used for any operation on the databases created using `PyMySql` Python Module

- `src/utils.py` contains:
    - dataclasses for the 3 entities used in the application


__Notes__

- each entity **(country, city, temperature)** has a dataclass and also a `RoutesManager`
- the arguments when receiving a request are checked for integrity and type
- have used a better precision on timestamp cause otherwise would have
duplicated entries in temperatures

__``mysql-db``__

- `database/` directory contains:
    - `init.sql` a file that is going to be sent to the mysql container when initializing the container to create the tables wanted

** I have implemented all tasks from the homework sheet.
