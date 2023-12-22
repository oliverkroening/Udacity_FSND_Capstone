from setting import DATABASE_URL
from sqlalchemy import String
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

database_path = DATABASE_URL
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    print(app.config["SQLALCHEMY_DATABASE_URI"]) 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
      db.create_all()

def db_drop_and_create_all():
    '''
    Function to drop the database tables and restart teh database to
    initialize a new database.
    '''
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    birthday = date(2001,1,1)
    actor = Actor(
        name = 'John Doe',
        date_of_birth = birthday.strftime('%d/%m/%Y'),
        gender = 'male'        
    )
    actor.insert()

'''
Association Tables
------
'''
actor_to_movies_table = db.Table(
  'actor_to_movies_table',
  db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
  db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)


'''
Movies
------
Attributes:
- id: Integer - id of movie's database entry
- title: String - title of the movie
- release_date: Integer - release year of the movie
Methods:
- __init__()
- insert()
- update()
- delete()
- format()
'''
class Movie(db.Model):  
  __tablename__ = 'movies'
  
  # define attributes
  id = db.Column(db.Integer, primary_key=True) 
  title = db.Column(db.String(256), nullable=False)
  release_date = db.Column(db.Integer, nullable=False)
  actors = db.relationship('Actor', secondary=actor_to_movies_table, 
                           backref=db.backref('movies', lazy=True))

  # define methods
  def __init__(self, title, release_date):
    '''
    Method for class "Movie" to initialize a database entry.
    INPUT:
    - id: Integer - id of movie's database entry
    - title: String - title of the movie
    - release_date: Integer - release year of the movie
    OUTPUT:
    - None
    '''
    self.title = title
    self.release_date = release_date
  
  def insert(self):
    '''
    Method for class "Movie" to add a new database entry.
    INPUT:
    - self: database object of Movie
    OUTPUT:
    - None
    '''
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    '''
    Method for class "Movie" to update a database entry.
    INPUT:
    - self: database object of Movie
    OUTPUT:
    - None
    '''
    db.session.commit()
  
  def delete(self):
    '''
    Method for class "Movie" to delete a database entry.
    INPUT:
    - self: database object of Movie
    OUTPUT:
    - None
    '''
    db.session.delete(self)
    db.session.commit()
  
  def short(self):
    '''
    Method for class "Movie" to represent a short representation of
    the database entry.
    INPUT:
    - self: database object of Movie
    OUTPUT:
    - None
    '''
    return {
      'id': self.id,
      'title': self.title}
  
  def format(self):
    '''
    Method for class "Movie" to represent a full database entry.
    INPUT:
    - self: database object of Movie
    OUTPUT:
    - None
    '''
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'actors': [actor.name for actor in self.actors]}


'''
Actors
------
Attributes:
- id: Integer - id of actor's database entry
- name: String - name of the actor
- date_of_birth: Date - date of birth of actor
- gender: String - gender of actor (male, female)
Methods:
- __init__()
- insert()
- update()
- delete()
- format()
'''
class Actor(db.Model):  
  __tablename__ = 'actors'
  
  # define attributes
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(String(256), nullable=False)
  date_of_birth = db.Column(db.DateTime, nullable=False)
  gender = db.Column(String(6), nullable=False)

  # define methods
  def __init__(self, name, date_of_birth, gender):
    '''
    Method for class "Actor" to initialize a database entry.
    INPUT:
    - id: Integer - id of actor's database entry
    - name: String - name of the actor
    - date_of_birth: Date - date of birth of actor
    - gender: String - gender of actor (male, female) 
    OUTPUT:
    - None
    '''
    self.name = name
    self.date_of_birth = date_of_birth
    self.gender = gender
  
  def insert(self):
    '''
    Method for class "Actor" to add a new database entry.
    INPUT:
    - self: database object of Actor
    OUTPUT:
    - None
    '''
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    '''
    Method for class "Actor" to update a database entry.
    INPUT:
    - self: database object of Actor
    OUTPUT:
    - None
    '''
    db.session.commit()
  
  def delete(self):
    '''
    Method for class "Actor" to delete a database entry.
    INPUT:
    - self: database object of Actor
    OUTPUT:
    - None
    '''
    db.session.delete(self)
    db.session.commit()

  def short(self):
    '''
    Method for class "Actor" to represent a short represenation of
    the database entry.
    INPUT:
    - self: database object of Actor
    OUTPUT:
    - None
    '''
    return {
      'id': self.id,
      'name': self.name}
  
  def format(self):
    '''
    Method for class "Actor" to represent a full database entry.
    INPUT:
    - self: database object of Actor
    OUTPUT:
    - None
    '''
    return {
      'id': self.id,
      'name': self.name,
      'date_of_birth': self.date_of_birth.strftime("%d/%m/%Y"),
      'gender': self.gender,
      'movies': [movie.title for movie in self.movies]}