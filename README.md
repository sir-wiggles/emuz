# Zume coding challange 

## About

Web application written in `Python3` using the `Flask` micro-framework to 
1. Get Star Wars movies grouped by their director.
2. Get a list of characters for a given film id


```
.
├── config.py           # config file, with such a simple app there's really nothing in there 
├── docker-compose.yml  # used to bring up the system if using the docker-compose method 
├── Dockerfile          # used by above
├── README.md           
├── requirements.txt    
├── run.py              # the start of the application
├── tests          
│   └── views.py       
└── zume
    ├── app.py          # route/view/error handling 
    └── __init__.py     # application initialization
```

## Running the application

I have two ways for you to run this application.  With `Docker` + `Docker Compose` or using your system's python

#### If using `Docker Compose`:
1. Within the root directory where you see the `docker-compose.yml` file execute `$ docker-compose up`.  
2. Wait for the containers to install and you should see something like the following logs appear
```
app_1  | [2017-08-28 07:17:30 +0000] [1] [INFO] Starting gunicorn 19.7.1
app_1  | [2017-08-28 07:17:30 +0000] [1] [INFO] Listening at: http://0.0.0.0:80 (1)
app_1  | [2017-08-28 07:17:30 +0000] [1] [INFO] Using worker: sync
app_1  | [2017-08-28 07:17:30 +0000] [8] [INFO] Booting worker with pid: 8
```
3. The exposed port is port `5000`


#### If using regular local `python`
1. Install packages `$ pip install -r requirements.txt`
2. Start the server `$ gunicorn  -b 0.0.0.0:5000 run:app`
3. Server listening on port `5000`


#### Running tests

A handfull of tests and all tests are mocked out so no external calls are being made to SWAPI

1. execute `nosetests tests/*`

## API

`GET /films`

```
$ curl localhost:5000/films -v
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /films HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.47.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: gunicorn/19.7.1
< Date: Mon, 28 Aug 2017 07:02:54 GMT
< Connection: close
< Content-Type: application/json
< Content-Length: 621
< 
{
  "George Lucas": [
    {
      "swapi_id": "1", 
      "title": "A New Hope"
    }, 
    {
      "swapi_id": "5", 
      "title": "Attack of the Clones"
    }, 
    {
      "swapi_id": "4", 
      "title": "The Phantom Menace"
    }, 
    {
      "swapi_id": "6", 
      "title": "Revenge of the Sith"
    }
  ], 
  "Irvin Kershner": [
    {
      "swapi_id": "2", 
      "title": "The Empire Strikes Back"
    }
  ], 
  "J. J. Abrams": [
    {
      "swapi_id": "7", 
      "title": "The Force Awakens"
    }
  ], 
  "Richard Marquand": [
    {
      "swapi_id": "3", 
      "title": "Return of the Jedi"
    }
  ]
}

```

`GET /characters/<int:swapi_id>` `swapi_id` can be found from the above api call

```
curl localhost:5000/characters/1 -v
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /characters/1 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.47.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: gunicorn/19.7.1
< Date: Mon, 28 Aug 2017 07:04:36 GMT
< Connection: close
< Content-Type: application/json
< Content-Length: 340
< 
[
  "Luke Skywalker", 
  "C-3PO", 
  "Darth Vader", 
  "R2-D2", 
  "Owen Lars", 
  "Leia Organa", 
  "R5-D4", 
  "Biggs Darklighter", 
  "Obi-Wan Kenobi", 
  "Beru Whitesun lars", 
  "Wilhuff Tarkin", 
  "Chewbacca", 
  "Han Solo", 
  "Greedo", 
  "Jabba Desilijic Tiure", 
  "Wedge Antilles", 
  "Raymus Antilles", 
  "Jek Tono Porkins"
]
```


