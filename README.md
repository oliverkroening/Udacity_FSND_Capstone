# Udacity_FSND_Capstone - Casting Agency API

This repository contains my solution for the Capstone project of Udacity's Full Stack Web Developer Nanodegree program.
The production app is hosted at Heroku: [https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/](https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/)
You can also run the app locally: [http://localhost:5000](http://localhost:5000)

### Project description
The project aims to create an API and model a database for a casting agency that is responsible for creating movies and managing and assigning actors to those movies. 
We have been put in the role of an Executive Producer within the company to create a system to simplify and streamline this process.

### Project requirements
The finalized code should be able to fulfill the following requirements:
1. *Models*: The code should model movies with attributes title and release date and actors with attributes name, age and gender in the database.
2. *API endpoints*: The code should have API endpoint for the following HTTP-Methods:
- `GET` /actors and /movies
- `DELETE` /actors/ and /movies/
- `POST` /actors and /movies and
- `PATCH` /actors/ and /movies/
3. *Roles*: The code should consider the following roles with there respective permissions:
- Casting Assistant: can view actors and movies
- Casting Director: has all permissions a Casting Assistant has and can add or delete an actor from the database as well as modify actors or movies
- Executive Producer: has all permissions a Casting Director has and can add or delete a movie from the database
4. *Tests*: The code should provide tests for success behavior of each endpoint, error behavior of each endpoint and at least two tests of RBAC for each role.

## Getting Started
### Installing Dependencies

1. **Python 3.12.1** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.
4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the PostgreSQL database. You'll primarily work in `app.py` and can reference `models.py`.

### Database Setup
With Postgres running, restore a database using the `movie_actors.psql` file provided. From the backend folder in terminal run:
```bash
drobdb -U postgres postgres
createdb -U postgres -E utf8 postgres
psql -U postgres postgres < movie_actors.psql
```
This will also add test data to the database. It will also ensure that UTF-8 encoding is used.

You can test the database by accessing it via
```bash
psql -U postgres postgres
```
and run the following command to generate an output of the database:
```bash
SELECT actors.name, actors.date_of_birth, actors.gender
FROM actors
JOIN actor_to_movies_table ON actors.id = actor_to_movies_table.actor_id
JOIN movies ON movies.id = actor_to_movies_table.movie_id
WHERE movies.title = 'The Dark Knight';
```
** Hint:** Make sure to store your database URL in the environment variables
```bash
export DATABASE_URL=<path-to-your-database>
```
The path should look like this `postgresql://<DB-User>:<DB-Password>@<host>:5432/<DB-Name>`.
In the case above and if you are running the app locally is should be: `postgresql://postgres:<DB-Password>@localhost:5432/postgres`


### Running the server

You can run the server locally by initializing the database:
```bash
python manage.py init
python manage.py migrate
python manage.py update
```
and run the `app.py`file:
```bash
python app.py
```
Make sure that the `app.py` is located in the root directory.
On the initial run, uncomment the line `db_drop_and_create_all()` to setup the required tables in the database.

## Database structure
The database for this Casting Agency API consists of two main tables: `actors` and `movies`. 
Additionally, there is an association table, `actor_to_movies_table`, to establish a many-to-many relationship between actors and movies.

These tables are created and managed using SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) for Python. The database structure allows for flexibility in associating actors with movies and vice versa.

####  Actors Table
- Table name: `actors`
- `id`: Integer - Primary key for the actor
- `name`: String - Name of the actor
- `date_of_birth`: Date - Date of birth of the actor
- `gender`: String - Gender of the actor (e.g., "Male" or "Female")

#### Movies Table
- Table name: `movies`
- `id`: Integer - Primary key for the movie
- `title`: String - Title of the movie
- `release_date`: Integer - Release year of the movie

#### actor_to_movies_table (Association Table)
This table establishes a many-to-many relationship between actors and movies.
- `movie_id`: Integer - Foreign key referencing the id column in the movies table.
- `actor_id`: Integer - Foreign key referencing the id column in the actors table.

## API Documentation

### Authentication
This application requires authentication to perform all CRUD actions to the database. All the endpoints require various permissions. The permissions are passed via Bearer tokens
**Auth0** is used to provide Third-Party Authentication.

### Authorization
All users, roles and permissions are managed Auth0.
Here, the following permissions and roles are defined:
#### Role: CastingAssistant
The role has the following permissions:
- `get:actors`: View actors
- `get:movies`: View movies

#### Role: CastingDirector
The role has the following permissions:
- `get:actors`: View actors
- `get:movies`: View movies
- `delete:actors`: Remove actors from database
- `patch:actors`: Update actors in database
- `patch:movies`: Update movies in database
- `post:actors`: Add actors to database

#### Role: ExecutiveDirector
The role has the following permissions:
- `get:actors`: View actors
- `get:movies`: View movies
- `delete:actors`: Remove actors from database
- `delete:movies`: Remove movies from database
- `patch:actors`: Update actors in database
- `patch:movies`: Update movies in database
- `post:actors`: Add actors to database
- `post:movies`: Add movies to database


### API Endpoints

#### GET `/`
- **Description**
  - Root endpoint that is provided to the public to make sure the app is running.

- **Required Permissions**
  - No authentication required.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/`
<details>
<summary>Sample Response</summary>
```
{
    "hello": "Hello!!!!! You are doing great in this Udacity project."
}
```
</details>

#### GET `/actors`
- **Description**
  - API endpoint that contains the `data.short()` data representation of all actors in the database ordered by id.

- **Required Permissions**
  - The user must have the permission `get:actors` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/actors`

<details>
<summary>Sample Response</summary>
```
{
    "actors": [
        {
            "id": 2,
            "name": "Morgan Freeman"
        },
        {
            "id": 3,
            "name": "Marlon Brando"
        },
        {
            "id": 5,
            "name": "Robert De Niro"
        },
        {
            "id": 7,
            "name": "Heath Ledger"
        },
        {
            "id": 8,
            "name": "Arnold Schwarzenegger"
        },
        {
            "id": 10,
            "name": "Leonardo DiCaprio"
        },
        {
            "id": 1,
            "name": "Timothy Francis Robbins"
        },
        {
            "id": 11,
            "name": "Leonardo DiCaprio"
        },
        {
            "id": 4,
            "name": "Alfredo James Pacino"
        }
    ],
    "success": true
}
```
</details>

#### GET `/actors/<int:actor_id>`
- **Description**
  - API endpoint that contains the `data.format()` data representation of a specific actor in the database by a given id.

- **Required Permissions**
  - The user must have the permission `get:actors` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/actors/1`
<details>
<summary>Sample Response</summary>
```
{
    "actor": {
        "date_of_birth": "16/10/1958",
        "gender": "Male",
        "id": 1,
        "movies": [
            "The Shawshank Redemption"
        ],
        "name": "Tim Robbins"
    },
    "success": true
}
```
</details>

#### DELETE `/actors/<int:actor_id>`
- **Description**
  - API endpoint to remove a specific actor from the database by id.

- **Required Permissions**
  - The user must have the permission `delete:actors` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/actors/7`
<details>
<summary>Sample Response</summary>
```
{
    "deleted_actor": 7,
    "success": true
}
```
</details>

#### POST `/actors`
- **Description**
  - API endpoint that allows authorized users to add a new row in the actors table in the database.

- **Required Permissions**
  - The user must have the permission `post:actors` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/actors`
  - Request body:
  - ```
{
    "name": "Leonardo DiCaprio",
    "date_of_birth": "11/11/1974",
    "gender": "Male"
}
```
<details>
<summary>Sample Response</summary>
```
{
    "new_actor": {
        "date_of_birth": "11/11/1974",
        "gender": "Male",
        "id": 12,
        "movies": [],
        "name": "Leonardo DiCaprio"
    },
    "success": true
}
```
</details>

#### PATCH `/actors/<int:actor_id>`
- **Description**
  - API endpoint that allows authorized users to update a specific entry in the actors table in the database.

- **Required Permissions**
  - The user must have the permission `patch:actors` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/actors/1`
  - Request body:
  - ```
{
    "name": "Timothy Francis Robbins"
}
```
<details>
<summary>Sample Response</summary>
```
{
    "edited_actor": {
        "date_of_birth": "16/10/1958",
        "gender": "Male",
        "id": 1,
        "movies": [
            "The Shawshank Redemption"
        ],
        "name": "Timothy Francis Robbins"
    },
    "success": true
}
```
</details>

#### GET `/movies`
- **Description**
  - API endpoint that contains the `data.short()` data representation of all movies in the database ordered by id.

- **Required Permissions**
  - The user must have the permission `get:movies` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/movies`

<details>
<summary>Sample Response</summary>
```
{
    "movies": [
        {
            "id": 1,
            "title": "The Shawshank Redemption"
        },
        {
            "id": 2,
            "title": "The Godfather"
        },
        {
            "id": 3,
            "title": "The Godfather: Part II"
        },
        {
            "id": 4,
            "title": "The Dark Knight"
        },
        {
            "id": 5,
            "title": "12 Angry Men"
        },
        {
            "id": 6,
            "title": "Schindler's List"
        },
        {
            "id": 7,
            "title": "The Lord of the Rings: The Return of the King"
        },
        {
            "id": 8,
            "title": "Pulp Fiction"
        },
        {
            "id": 9,
            "title": "The Good, the Bad and the Ugly"
        },
        {
            "id": 10,
            "title": "Fight Club"
        }
    ],
    "success": true
}
```
</details>

#### GET `/movies/<int:movies_id>`
- **Description**
  - API endpoint that contains the `data.format()` data representation of a specific movie in the database by a given id.

- **Required Permissions**
  - The user must have the permission `get:movies` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/movies/1`
<details>
<summary>Sample Response</summary>
```
{
    "movie": {
        "actors": [
            "Morgan Freeman",
            "Timothy Francis Robbins"
        ],
        "id": 1,
        "release_date": 1994,
        "title": "The Shawshank Redemption"
    },
    "success": true
}
```
</details>

#### DELETE `/movies/<int:movie_id>`
- **Description**
  - API endpoint to remove a specific movies from the database by id.

- **Required Permissions**
  - The user must have the permission `delete:movies` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/movies/1`
<details>
<summary>Sample Response</summary>
```
{
    "deleted_movie": 1,
    "success": true
}
```
</details>

#### POST `/movies`
- **Description**
  - API endpoint that allows authorized users to add a new row in the movies table in the database.

- **Required Permissions**
  - The user must have the permission `post:movies` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/movies`
  - Request body:
  - ```
{
    "title": "Django Unchained",
    "release_date": 2012,
    "actors": ["Leonardo DiCaprio"]
}
```
<details>
<summary>Sample Response</summary>
```
{
    "new_movie": {
        "actors": [
            "Leonardo DiCaprio"
        ],
        "id": 33,
        "release_date": 2012,
        "title": "Django Unchained"
    },
    "success": true
}
```
</details>

#### PATCH `/movies/<int:movie_id>`
- **Description**
  - API endpoint that allows authorized users to update a specific entry in the movies table in the database.

- **Required Permissions**
  - The user must have the permission `patch:movies` to perform the call on this endpoint.

- **Sample Request**
  - `https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/movies/16`
  - Request body:
  - ```
{
    "actors": ["Robert De Niro"]
}
```
<details>
<summary>Sample Response</summary>
```
{
    "edited_movie": {
        "actors": [
            "Robert De Niro"
        ],
        "id": 16,
        "release_date": 1990,
        "title": "Goodfellas"
    },
    "success": true
}
```
</details>

### Error Handling
Errors are returned in the following JSON format:
```
{
    'success': False,
    'error': error.status_code,
    'message': error.error['description']
}
```

The API returns the following types of error:
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Testing
To run the tests, run
```
drobdb -U postgres postgres_test
createdb -U postgres -E utf8 postgres_test
psql -U postgres postgres_test < movie_actors.psql
python test.py
```
The file `test.py`contains one test for success and one test for error behavior for each end point and also tests the authorization within the error behavior.

Additionally, a postman collection (`udacity-fsnd-capstone.postman_collection.json`) was added to run tests locally.
The collection contains tests for each role and endpoint to perform the calls.

## Author and Acknowledgement
Oliver Kröning contributed to all files within this project with exception of the following files, which were provided by [Udacity](https://www.udacity.com/):
- `Procfile`
- `setup.sh`
- `manage.py`











  
