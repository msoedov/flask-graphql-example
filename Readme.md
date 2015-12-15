Example of small GraphQL app with Flask + Python3/PyPy3 + MongoDb

[![Build Status](https://travis-ci.org/msoedov/flask-graphql-example.svg?branch=master)](https://travis-ci.org/msoedov/flask-graphql-example)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/44eede68b96745bdafee5a8a208ea3c3/badge.svg)](https://www.quantifiedcode.com/app/project/44eede68b96745bdafee5a8a208ea3c3)

### Quick start with docker


```shell
docker-compose build
docker-compose up
```

Optionally populate database

```shell
docker-compose run web pypy3 manage.py init
```

And then open http://localhost:5000/ui


![Demo screen](https://sc-cdn.scaleengine.net/i/1abd73bf614838ef8cae5a35093ca3cd1.png)


### Development workflow

Create a virtual environment with Python3 or PyPy3

Make sure you have running MongoDb instance either on localhost or
```shell
export DB_PORT_27017_TCP_ADDR='ip address'

```

Likewise you can use containerized  Mongo but you will need to setup env variables as well

```shell
docker-compose build
docker-compose up db
```


Then you can install deps and run the python app
```
make req
python api.py
```

#### Miscellaneous

Auto format your code
```shell

make format
```

Nosetests with reload
```shell
make watch
```