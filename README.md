# SIMPLE API WITH DJANGO REST FRAMEWORK
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

## Requirements
- Python 3.12.4
- Django 4.1.13
- Django REST Framework
- Djongo

## Installation
After cloned the repository, please create a virtual environment, so you have a clean python installation.

You can do this by running the command
```
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have one single resource, `songs`, so we will use the following URLS - `/songs/` and `/songs/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`songs` | GET | READ | Get all songs
`songs/:id` | GET | READ | Get a single song
`songs`| POST | CREATE | Create a new song
`songs/:id` | PATCH | UPDATE | Update a song
`songs/:id` | DELETE | DELETE | Delete a song

## Use
We can test the API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/jakubroztocil/httpie#installation), or we can use [Postman](https://www.postman.com/).

## Users Sign Up and Sign In

### Sign up a user
```
POST http://localhost:8000/v1/account/signup
```
```json
{
    "email": "email@email.com",
    "password": "password"
}
```

### Sign in
```
POST http://localhost:8000/v1/account/login
```
```JSON
{
    "email": "email@email.com",
    "password": "password"
}
```
Response
```JSON
{
    "userId": "66a5dd5af14f86b95db29393",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

### Requesting New Access Token
```
POST http://localhost:8000/v1/auth/token/refresh
```
```JSON
{
    "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
}
```
and we will get a new access token
```JSON
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```

## Commands

### Get all songs
```
GET http://localhost:8000/v1/songs
Header: "Authorization: Bearer {YOUR_TOKEN}"
```
### Get a single song
```
GET http://localhost:8000/v1/songs/{song_id}
Header: "Authorization: Bearer {YOUR_TOKEN}"
```
### Create a new song
```
POST http://localhost:8000/v1/songs
Header: "Authorization: Bearer {YOUR_TOKEN}"
```
```JSON
{
    "title": "Here I am",
    "album": "Spirit",
    "singer": "Bryan Adams",
    "genre": "Rock",
    "year": 2002
}
```
### Patch a song
```
PATCH http://localhost:8000/v1/songs/{song_id}
Header: "Authorization: Bearer {YOUR_TOKEN}"
```
```JSON
{
    "album": "Spirit: Stallion of the Cimarron"
}
```

### Delete a song
```
DELETE http://localhost:8000/v1/songs/{song_id}
Header: "Authorization: Bearer {YOUR_TOKEN}"
```

### Pagination
The API supports pagination, by default responses have a page_size=10 but if you want change that you can pass through params page_size={your_page_size_number}
```
GET http://localhost:8000/v1/songs?page=1
Header "Authorization: Bearer {YOUR_TOKEN}"

GET http://localhost:8000/v1/songs?page=3
Header "Authorization: Bearer {YOUR_TOKEN}"

GET http://localhost:8000/v1/songs?page=3&page_size=15
Header "Authorization: Bearer {YOUR_TOKEN}"
```

### Filters
The API supports filtering, you can filter by the attributes of a song like this
```
GET http://localhost:8000/v1/songs?title="Here I am"
Header: "Authorization: Bearer {YOUR_TOKEN}"

GET http://localhost:8000/v1/songs?year=2020
Header: "Authorization: Bearer {YOUR_TOKEN}"

GET http://localhost:8000/v1/songs?year__gt=2002&year__lt=2022
Header: "Authorization: Bearer {YOUR_TOKEN}"

GET http://localhost:8000/v1/songs?genre="Rock"
Header: "Authorization: Bearer {YOUR_TOKEN}"
```
