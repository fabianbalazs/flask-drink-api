# Flask Drink API

A simple REST API built with Python and Flask for managing drinks.

This project was created as a learning exercise to understand how backend web applications work, including REST API design, database models, and CRUD operations using SQLAlchemy.

## Features

* Retrieve a list of drinks
* Get a specific drink by ID
* Add a new drink to the database
* Delete a drink
* SQLite database integration



## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* REST API



## Project Structure

```
flask-drink-api
│
├── app.py            # Main application and API routes
├── models.py         # Database models
├── config.py         # Application configuration
├── requirements.txt  # Project dependencies
├── README.md         # Project documentation
└── .gitignore        # Ignored files for Git
```



## Installation

Clone the repository:

```
git clone https://github.com/fabianbalazs/flask-drink-api.git
```

Navigate into the project folder:

```
cd flask-drink-api
```

Install the dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python app.py
```



## API Endpoints

### Get all drinks

GET /drinks

Returns a list of all drinks stored in the database.

Example response:

```
{
  "drinks": [
    {
      "name": "Cola",
      "description": "Sweet carbonated drink"
    }
  ]
}
```



### Get a single drink

GET /drinks/<id>

Returns a single drink by its ID.


### Add a drink

POST /drinks

Example request body:

```
{
  "name": "Orange Juice",
  "description": "Fresh squeezed orange juice"
}
```


### Delete a drink

DELETE /drinks/<id>

Deletes a drink from the database.


## Learning Goals

This project helped me practice:

* Building REST APIs with Flask
* Working with databases using SQLAlchemy
* Designing backend endpoints
* Structuring a Python backend project
* Using Git and GitHub for version control


## Future Improvements

Possible future improvements for this project:

* Add update (PUT) endpoint
* Add input validation
* Improve error handling
* Add authentication
* Create a frontend interface



## Author

Created as part of my backend development learning journey.
