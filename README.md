# Udacity_FSND_Capstone - Casting Agency API

This repository contains my solution for the Capstone project of Udacity's Full Stack Web Developer Nanodegree program.
The production app is hosted at Heroku: [https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/](https://myfsnd-capstone-app-82599-1d98d9dff28c.herokuapp.com/)
You can also run the app locally: [http://localhost:5000](http://localhost:5000)

The project aims to create an API and model a database for a casting agency that is responsible for creating movies and managing and assigning actors to those movies. 
We have been put in the role of an Executive Producer within the company to create a system to simplify and streamline this process.
The finalized code should be able to fulfill the following requirements:
1. Models: The code should model movies with attributes title and release date and actors with attributes name, age and gender in the database.
2. API endpoints: The code should have API endpoint for the following HTTP-Methods:
- `GET` /actors and /movies
- `DELETE` /actors/ and /movies/
- `POST` /actors and /movies and
- `PATCH` /actors/ and /movies/
3. Roles: The code should consider the following roles with there respective permissions:
- Casting Assistant: can view actors and movies
- Casting Director: has all permissions a Casting Assistant has and can add or delete an actor from the database as well as modify actors or movies
- Executive Producer: has all permissions a Casting Director has and can add or delete a movie from the database
4. Tests: The code should provide tests for success behavior of each endpoint, error behavior of each endpoint and at least two tests of RBAC for each role.

## Getting Started
### Installing Dependencies
