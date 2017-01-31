# Using APIs built with sanic_crud

sanic_crud creates a standard REST API that allows direct manipulation of the database. The following methods are
supported: [GET, POST, PUT, DELETE]

There are 2 types of resources (endpoints) available, Single Resources and Collection Resources.
  * Single Resources only support **[GET, PUT, DELETE]**
  * Collection Resources only support **[GET, POST]**

## Single Resource ([GET, PUT, DELETE])
A Single Resource is what it sounds like. A single resources or row from the database. It is accessed by navigating to
the `/{tablename}/{primary_key}` endpoint.

#### GET Request
For Example a **GET** request to `http://127.0.0.1:8000/person/1` might return:

  ```json
  {
     "data": {
       "id": 1,
       "name": "Sanic the Hedgehog",
       "email": "sanic@gmail.com",
       "create_datetime": null
     },
     "status_code": 200,
     "message": "OK"
   }
  ```

#### PUT Request
You could also update this record with a **PUT** request with the following JSON:

  ```json
  {
   "email": "new_email@gmail.com"
  }
  ```
   
This will update the record in the database and will also return the new object:
    
  ```json
  {
    "data": {
      "id": 1,
      "name": "Sanic the Hedgehog",
      "email": "new_email@gmail.com",
      "create_datetime": null
    },
    "status_code": 200,
    "message": "OK"
  }
  ```

#### DELETE Request
You can also send a **DELETE** request to the endpoint to delete the record from the database

  ```json
  {
    "data": null,
    "status_code": 200,
    "message": "Resource with id '1' was deleted!"
  }
  ```
  
## Collection Resource([GET, POST])
A Collection resource contains multiple database records or rows. It is accessed by navigating to:
`/{tablename}`

#### GET Request
For example a **GET** request to `http://127.0.0.1:8000/person` might return something like:

  ```json
  {
    "data": [
        {
            "id": 10,
            "name": "yee",
            "email": "yee@yee.com",
            "create_datetime": null
        },
        {
            "id": 11,
            "name": "Sanic the Hedgehog",
            "email": "sanic@gmail.com",
            "create_datetime": 1483228800
        }
    ],
    "status_code": 200,
    "message": "OK",
    "page": 1,
    "total_pages": 1
  }
  ```
As you can see, there are also pages, you can see how many total pages there are as well as the current page.
The maximum entries per page is default to 100 but can be configured. To change pages, you can simply include `?page={pagenumber}`
in your url

You can also use query parameters as well. For example, if you wanted to find all records where the id is greater than 10
you would hit this endpoint `http://127.0.0.1/person?id__gt=10` and you would only get records with that. You can mix and match
and combine as many of these query paramters as you want.

For a full list of the query parameters and what they do, see the [Query Paramters Docs](query_parameters.md)

#### POST Request
A **POST** to this endpoint works very similar to a **PUT** with the exception of it creating records rather than updating them.

A response from a **POST** would look something like:

  ```json
  {
    "data": {
        "id": 12,
        "name": "Sanic the Hedgehog",
        "email": "new_email@gmail.com",
        "create_datetime": "2017-01-01 00:00:00"
    },
    "status_code": 200,
    "message": "Resource with id '12' was created!"
  }
  ```
  
## Messages
  
The API that is generated is fully fleshed out and contains correct error messaging and status codes.
If the user inputs a string where an int is expected, the API will return a message stating which field is incorrect
and what type it was expecting. For example, an incorrect datetime on our examples above, might show something like:

  ```json
  {
    "data": null,
    "status_code": 400,
    "message": "Value '00:00:00 01-01-2017' must be a datetime: YYYY-mm-dd HH:MM:SS or integer"
  }
  ```

**Next:** [Query Parameters](query_parameters.md)
