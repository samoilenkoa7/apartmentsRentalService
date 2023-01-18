# SIMPLE RENTAL/BOOKING SERVICE BASED ON DRF
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

## Requirements
- Python>=3.9
- Django>=4.1
- Django REST Framework

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv venv
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.


Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`api/v1/posts` | GET | READ | Get all rental posts with available time and pictures
`api/v1/posts/:id` | GET | READ | Get a single post with it available time and pictures 
`api/v1/posts/`| POST | CREATE | Create a new post
`api/v1/posts/:id` | DELETE | DELETE | Delete 

## Use
We can test the API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/jakubroztocil/httpie#installation), or we can use [Postman](https://www.postman.com/)

Httpie is a user-friendly http client that's written in Python. Let's try and install that.

You can install httpie using pip:
```
pip install httpie
```

First, we have to start up Django's development server.
```
python manage.py runserver
```
Only authenticated users can use the API services, for that reason if we try this:
```
http  http://127.0.0.1:8000/api/v1/movies/
```
we get:
```
{
    [
    {
        "pk": 16,
        "title": "From postman 2",
        "description": "From postman 2",
        "location": "From postman 2",
        "price": "123.00",
        "date": "2023-01-10T01:47:15.525901Z",
        "views": 8,
        "user": 1,
        "acc_pictures": [],
        "available_time": [
            {
                "id": 7,
                "time": "2023-01-10T19:23:00Z",
                "apartment": 16
            }
        ]
    },
    {
        "pk": 14,
        "title": "From postman 2",
        "description": "From postman 2",
        "location": "From postman 2",
        "price": "123.00",
        "date": "2023-01-09T07:01:01.086565Z",
        "views": 38,
        "user": 2,
        "acc_pictures": [],
        "available_time": [
            {
                "id": 2,
                "time": "2023-01-08T01:25:49Z",
                "apartment": 14
            }
        ]
    }
    }
```
Instead, if we try to access with credentials:
```
http http://127.0.0.1:8000/api/v1/post/ "Authorization: df128fbda1ee47512e81f87a5470b62c5300a863"
```
we get all posts that was posted bu user
```
{
        "pk": 9,
        "title": "Some post",
        "description": "Description",
        "location": "New York",
        "price": "123.00",
        "date": "2023-01-07T06:30:31.733399Z",
        "views": 34,
        "user": 2,
        "acc_pictures": [
            {
                "id": 8,
                "image_to_apartment": "/media/apps-pictures/2023/01/07/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2022-12-13_%D0%B2_16.10.50_zTK8Ts8.png",
                "pictures": 9
            }
        ],
        "available_time": []
    },
    {
        "pk": 2,
        "title": "some title",
        "description": "desc",
        "location": "Some location",
        "price": "123.00",
        "date": "2023-01-06T20:31:19.502976Z",
        "views": 0,
        "user": 2,
        "acc_pictures": [
            {
                "id": 11,
                "image_to_apartment": "/media/apps-pictures/2023/01/09/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2022-12-10_%D0%B2_14.14.54.png",
                "pictures": 2
            }
        ],
        "available_time": []
    }
```

## Create users and Tokens

First we need to create a user, so we can log in
```
http POST http://127.0.0.1:8000/api/v1/auth/register/ email="email@email.com" username="USERNAME" password="PASSWORD"
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http http://127.0.0.1:8000/api/v1/auth/token/login/ username="username" password="password"
```
after that, we get the token
```
{
    'Authorization': 'TOKEN'
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.


The API has some restrictions:
-   The posts are always associated with a creator (user who created it).
-   Only the creator of a post may update or delete it.

### Commands
```
Get all posts
http http://127.0.0.1:8000/api/v1/posts/ "Authorization: {YOUR_TOKEN}" 
Get a single post
http GET http://127.0.0.1:8000/api/v1/posts/{post_id}/ "Authorization: {YOUR_TOKEN}" 
Create a new post
http POST http://127.0.0.1:8000/api/v1/posts/ "Authorization: {YOUR_TOKEN}" title="Apartment in LA" description="Description" location="Los Angeles" price="300" views="0" user="1"  
Delete a post
http DELETE http://127.0.0.1:8000/api/v1/post/{post_id}/ "Authorization: {YOUR_TOKEN}"
```
