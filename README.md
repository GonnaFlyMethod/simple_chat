# simple_chat

---

## Getting Started

These instructions will help you to get the copy of the project for development and testing purposes.

## Running Locally

### Clone the project to your local machine

```
$ git clone https://github.com/GonnaFlyMethod/simple_chat
```

### Install poetry  
Poetry is a new dependencies manager for python. It's simple and clever. To install poetry run:

```
$ pip3 install poetry
```

### Activate poetry env
```
$ source $HOME/.poetry/env
$ cd simple_chat
$ poetry shell
```

### Install dependencies

```
$ poetry install
```

### Create .env file near the manage.py file 

***Note:*** .env will be invisible, so make it visible and set the following values inside: 

```
DEBUG=on
SECRET_KEY="dev"
DATABASE_URL=psql://test:test@127.0.0.1:5432/test
STATIC_URL=/static/
```

### Create database

```
$ sudo -u postgres psql
```
then:
```
CREATE DATABASE test;
```

### Create user in the DB 

```
CREATE USER test with encrypted password 'test';
```
Done! We have created a new user with the name "test" and password "test".

### Grant DB user

```
GRANT ALL PRIVILEGES ON DATABASE test TO test;

```

### Get Redis
```
$ sudo apt update
$ sudo apt install redis-server
```

### Run redis server
```
$ sudo systemctl daemon-reload
$ sudo systemctl start redis
```

### Run celery
```
$ celery -A core worker --loglevel=info
```

### Migrate data to the DB

```
$ python3 manage.py migrate
```

### Create a superuser
```
$ python3 manage.py createsuperuser
```

### Run project
```
$ python3 manage.py runserver
```
