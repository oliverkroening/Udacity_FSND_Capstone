import os
import sys
import json
#import syslog
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from database.models import setup_db, Actor, Movie, db_drop_and_create_all
from flask_cors import CORS
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    if test_config is None:
        setup_db(app)
    else:
        setup_db(app,test_config)
    CORS(app)

    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        '''
        Function to set the HTTP response headers and methods for a response
        after a request to control the access for resources.
        source: TRIVIA-App project in FSND

        Input: 
        - response (original response for a request)
        
        Output:
        - response (response with modified headers and methods)
        '''
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
            )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, PUT, POST, DELETE, OPTIONS'
            )
        return response

    @app.route('/')
    def get_greeting():
        '''
        Function to check the accessability!
        '''
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return jsonify({'hello': greeting}), 200
    
    '''
    API Endpoints to perform CRUD operations for Actors
    ---------------------------------------------------
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(jwt):
        '''
        API endpoint that contains the data.short() data representation 
        of all actors in the database ordered by id.

        Allowed HTTP methods:
            - GET - obtain all actors with data representation (data.short())

        Authorized user roles:
            - CastingAssistant
            - CastingDirector
            - ExecutiveProducer

        Required Permissions: 
            - get:actors
        
        Requested Parameters:
            - jwt - token to check for permissions

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "actors": list - list of data representations of all actors
        '''
        # query all actors that are stored in the database
        actors_all = Actor.query.all()
        
        # return 404 - Not found, in case there are no actors in the database
        if actors_all is None:
            abort(404)

        # perform actors.short() to obtain the data representation of all actors
        actors = [actor.short() for actor in actors_all]

        # return json with data representions
        return jsonify({
            "success": True,
            "actors": actors
        }), 200
    
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth("get:actors")
    def get_actor_detail(jwt, actor_id):
        '''
        API endpoint that contains the data.format() data representation 
        of a specific actor in the database by a given id.

        Allowed HTTP methods:
            - GET - obtain a specific actor with data representation 
                    (data.format())

        Authorized user roles:
            - CastingAssistant
            - CastingDirector
            - Executive Producer

        Required Permissions: 
            - get:actors
        
        Requested Parameters:
            - jwt - token to check for permissions
            - actor_id - ID of actor in the database

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "actor": data representation of a specific actor
        '''
        # query actor by actor_id
        actor = Actor.query.get(actor_id)
        
        # return 404 - Not found, in case there are no actor with this id
        if actor is None:
            abort(404)

        # return json with data representions
        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(jwt, actor_id):
        '''
        API endpoint to remove a specific actor from the database by id.

        Allowed HTTP methods:
            - DELETE - delete specific actor from database

        Authorized user roles:
            - CastingDirector
            - Executive Producer

        Required Permissions: 
            - delete:actors
        
        Requested Parameters:
            - jwt - token to check for permissions
            - actor_id - ID of actor in the database
            
        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "deleted_actor": id of deleted actor
        '''
        try:
            # query actor by actor_id
            actor = Actor.query.get(actor_id)
            
            # return 404 - Not found, in case there are no actor with this id
            if actor is None:
                abort(404)

            # delete actor
            actor.delete()

            # return json
            return jsonify({
                "success": True,
                "deleted_actor": actor_id
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)
    
    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actors")
    def create_actor(jwt):
        '''
        API endpoint that allows authorized users to a new row in the actors table 
        in the database.

        Allowed HTTP methods:
            - POST - create a new actor in the database

        Authorized user roles:
            - CastingDirector
            - Executive Producer

        Required Permissions: 
            - post:actors
        
        Requested Parameters:
            - jwt - token to check for permissions

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "new_actor": data representation of a created actor
        '''
        
        # get json from request
        data = request.get_json()
        
        # raise 422 error in case there is no data that could be extracted 
        # from the request
        if data is None:
            abort(422)
        
        # extract information from request data
        name = data.get('name', None)
        date_of_birth = data.get('date_of_birth', None)
        gender = data.get('gender', None)

        # raise 422 error in case the required data is not in the request
        if (name is None) or (date_of_birth is None) or (gender is None):
            abort(422)

        # create new Actor object from extracted data
        try:
            new_actor = Actor(
                name = name,
                date_of_birth = date_of_birth,
                gender = gender
            )
            # insert new actor in database
            new_actor.insert()
            # return json with data representions
            return jsonify({
                "success": True,
                "new_actor": new_actor.format()
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor(jwt, actor_id):
        '''
        API endpoint that allows authorized users to a update a specific entry 
        in the actors table in the database.

        Allowed HTTP methods:
            - PATCH - edit and update an actor in the database

        Authorized user roles:
            - CastingDirector
            - Executive Producer

        Required Permissions: 
            - patch:actors
        
        Requested Parameters:
            - jwt - token to check for permissions
            - actor_id - ID of actor in the database

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "edited_actor": data representation of a edited actor
        '''
        
        # get json from request
        data = request.get_json()
        
        # raise 422 error in case there is no data that could be extracted 
        # from the request
        if data is None:
            abort(422)
        
        try:
            # get Actor object from database by id
            actor = Actor.query.get(actor_id)
            
            # return 404 - Not found, in case there are no actor with this id
            if actor is None:
                abort(404)
            
            # extract data from request data and assign extracted data to 
            # database entry
            if "name" in data:
                name = data.get('name', None)
                actor.name = name
            
            if "date_of_birth" in data:
                date_of_birth = data.get('date_of_birth', None)
                actor.date_of_birth = date_of_birth
            
            if "gender" in data:
                gender = data.get('gender', None)
                actor.gender = gender
            
            # update actor in database
            actor.update()

            # return json with data representions
            return jsonify({
                "success": True,
                "edited_actor": actor.format()
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)
    

    '''
    API Endpoints to perform CRUD operations for Movies
    ---------------------------------------------------
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(jwt):
        '''
        API endpoint that contains the data.short() data representation 
        of all movies in the database ordered by id.

        Allowed HTTP methods:
            - GET - obtain all movies with data representation (data.short())

        Authorized user roles:
            - CastingAssistant
            - CastingDirector
            - Executive Producer

        Required Permissions:  
            - get:movies

        Requested Parameters:
            - jwt - token to check for permissions

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "movies": list - list of data representations of all movies
        '''
        # query all movies that are stored in the database
        movies_all = Movie.query.all()
        
        # return 404 - Not found, in case there are no movies in the database
        if movies_all is None:
            abort(404)

        # perform movies.short() to obtain the data representation of all movies
        movies = [movie.short() for movie in movies_all]

        # return json with data representions
        return jsonify({
            "success": True,
            "movies": movies
        }), 200
    
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth("get:movies")
    def get_movie_detail(jwt, movie_id):
        '''
        API endpoint that contains the data.format() data representation 
        of a specific movie in the database by a given id.

        Allowed HTTP methods:
            - GET - obtain a specific movie with data representation 
                    (data.format())

        Authorized user roles:
            - CastingAssistant
            - CastingDirector
            - Executive Producer

        Required Permissions:  
            - get:movies
        
        Requested Parameters:
            - jwt - token to check for permissions
            - movie_id - ID of movie in the database

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "movie": data representation of a specific movie
        '''
        # query movie by movie_id
        movie = Movie.query.get(movie_id)
        
        # return 404 - Not found, in case there are no movie with this id
        if movie is None:
            abort(404)

        # return json with data representions
        return jsonify({
            "success": True,
            "movie": movie.format()
        }), 200
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(jwt, movie_id):
        '''
        API endpoint to remove a specific movie from the database by id.

        Allowed HTTP methods:
            - DELETE - delete specific movie from database

        Authorized user roles:
            - Executive Producer

        Required Permissions: 
            - delete:movies
        
        Requested Parameters:
            - jwt - token to check for permissions
            - movie_id - ID of movie in the database

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "deleted_movie": id of deleted movie
        '''
        try:
            # query movie by movie_id
            movie = Movie.query.get(movie_id)
            
            # return 404 - Not found, in case there are no movie with this id
            if movie is None:
                abort(404)

            # delete movie
            movie.delete()

            # return json
            return jsonify({
                "success": True,
                "deleted_movie": movie_id
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)
    
    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def create_movie(jwt):
        '''
        API endpoint that allows authorized users to a new row in the movies table 
        in the database.

        Allowed HTTP methods:
            - POST - create a new movie in the database

        Authorized user roles:
            - Executive Producer

        Required Permissions: 
            - post:movies
        
        Requested Parameters:
            - jwt - token to check for permissions

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "new_movie": data representation of a created movie
        '''
        
        # get json from request
        data = request.get_json()
        
        # raise 422 error in case there is no data that could be extracted 
        # from the request
        if data is None:
            abort(422)
        
        # extract information from request data
        title = data.get('title', None)
        release_date = data.get('release_date', None)
        actors = data.get('actors', None)

        # raise 422 error in case the required data is not in the request
        if (title is None) or (release_date is None) or (len(actors) == 0):
            abort(422)

        # create new Movie object from extracted data
        try:
            new_movie = Movie(
                title = title,
                release_date = release_date
            )

            for actor_name in actors:
                actor = Actor.query.filter_by(name=actor_name).first()
                if actor is None:
                # Actor does not exist and should be added first
                    abort(404)
                new_movie.actors.append(actor)
                
            # insert new movie in database
            new_movie.insert()

            # return json with data representions
            return jsonify({
                "success": True,
                "new_movie": new_movie.format()
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie(jwt, movie_id):
        '''
        API endpoint that allows authorized users to a update a specific entry 
        in the movies table in the database.

        Allowed HTTP methods:
            - PATCH - edit and update a movie in the database

        Authorized user roles:
            - CastingDirector
            - Executive Producer

        Required Permissions: 
            - patch:movies
        
        Requested Parameters:
            - jwt - token to check for permissions
            - movie_id - ID of movie in the database

        Returned Parameters:
            - "success": boolean - information, if request was successful
            - "edited_movie": data representation of a edited movie
        '''
        
        # get json from request
        data = request.get_json()
        
        # raise 422 error in case there is no data that could be extracted 
        # from the request
        if data is None:
            abort(422)
        
        try:
            # get Movie object from database by id
            movie = Movie.query.get(movie_id)
            
            # return 404 - Not found, in case there are no movies with this id
            if movie is None:
                abort(404)
            
            # extract data from request data and assign extracted data to 
            # database entry
            if "title" in data:
                title = data.get('title', None)
                movie.title = title
            
            if "release_date" in data:
                release_date = data.get('release_date', None)
                movie.release_date = release_date
            
            if "actors" in data:
                actors = data.get('actors', None)
                # raise 422 error in case the actors list is empty
                if len(actors) == 0:
                    abort(422)
                
                for actor_name in actors:
                    actor = Actor.query.filter_by(name=actor_name).first()
                    if actor is None:
                    # Actor does not exist and should be added first
                        abort(404)
                    movie.actors.append(actor)
            
            # update movie in database
            movie.update()

            # return json with data representions
            return jsonify({
                "success": True,
                "edited_movie": movie.format()
            }), 200
        
        except:
            # raise 400 error in case of bad request during the
            # database operation
            # print error information
            print(sys.exc_info())
            abort(400)

    '''
    Error Handling
    ---------------------------------------------------
    '''
    
    @app.errorhandler(400)
    def error_handler_bad_request(error):
        '''
        Error handling function for error 
        - 400 "bad request"
        '''
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        }), 400
    
    @app.errorhandler(401)
    def error_handler_unauthorized(error):
        '''
        Error handling function for error 
        - 401 "Unauthorized"
        '''
        return jsonify({
            'success': False,
            'error': 401,
            'message': "Unauthorized"
        }), 401
    
    @app.errorhandler(403)
    def error_handler_forbidden(error):
        '''
        Error handling function for error 
        - 403 "Forbidden"
        '''
        return jsonify({
            'success': False,
            'error': 403,
            'message': "Forbidden"
        }), 403
    
    @app.errorhandler(404)
    def error_handler_not_found(error):
        '''
        Error handling function for error 
        - 404 "Not Found"
        '''
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404
    
    @app.errorhandler(422)
    def error_handler_unprocessable(error):
        '''
        Error handling function for error 
        - 422 "Unprocessable"
        '''
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def error_handler_internal_server_error(error):
        '''
        Error handling function for error 
        - 500 "Internal Server Error"
        '''
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500
    
    @app.errorhandler(AuthError)
    def error_handler_autherror(error):
        '''
        Error handling function for error
        - AuthError "authorization error"
        '''
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
