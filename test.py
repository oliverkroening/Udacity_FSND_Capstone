import os
import unittest
import json
from setting import DATABASE_URL_TEST, \
    casting_assistant_token, \
    casting_director_token, \
    executive_director_token
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, Actor, Movie

class CastingAgencyTestCase(unittest.TestCase):
    '''
    Class representing the test case for the Casting Agency app.
    '''
    def setUp(self):
        '''
        Function to set up the tests and define the required variables.
        '''
        self.databast_path = DATABASE_URL_TEST
        self.app = create_app(self.databast_path)
        self.client = self.app.test_client
        self.casting_assistant_token = casting_assistant_token
        self.casting_director_token = casting_director_token
        self.executive_producer_token = executive_director_token

    def tearDown(self):
        '''
        Executed after reach test
        '''
        pass

    ### --------------------------------------------
    ### Tests according to function: get_actors()
    ### --------------------------------------------

    # Test success behavior for the get_actors endpoint

    def test_get_actors_success(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {self.casting_assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    # Test error behavior for the get_actors endpoint

    def test_get_actors_error(self):
        response = self.client().get(
            '/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    ### --------------------------------------------
    ### Tests according to function: get_actor_detail()
    ### --------------------------------------------
    
    # Test success behavior for the get_actor_detail endpoint

    def test_get_actor_detail_success(self):
        # Assuming actor_id 1 exists in the database
        response = self.client().get(
            '/actors/1',
            headers={'Authorization': f'Bearer {self.casting_assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['actor'])

    # Test error behavior for the get_actor_detail endpoint

    def test_get_actor_detail_error(self):
        # Assuming actor_id 999 does not exist in the database
        response = self.client().get(
            '/actors/999',
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: delete_actor()
    ### --------------------------------------------
    
    # Test success behavior for the delete_actor endpoint

    def test_delete_actor_success(self):
        # Assuming actor_id 9 exists in the database
        response = self.client().delete(
            '/actors/9',
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_actor'], 9)

    # Test error behavior for the delete_actor endpoint

    def test_delete_actor_error(self):
        # Assuming actor_id 999 does not exist in the database
        response = self.client().delete(
            '/actors/999',
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: create_actor()
    ### --------------------------------------------
    
    # Test success behavior for the create_actor endpoint

    def test_create_actor_success(self):
        actor_data = {
            'name': 'John Doe',
            'date_of_birth': '2001-01-01',
            'gender': 'Male'
        }
        response = self.client().post(
            '/actors',
            json=actor_data,
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('new_actor', data)

    # Test error behavior for the create_actor endpoint

    def test_create_actor_error(self):
        # Missing 'gender' field in the actor data
        actor_data = {
            'name': 'Jane Doe',
            'date_of_birth': '1990-01-01'
        }
        response = self.client().post(
            '/actors',
            json=actor_data,
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: update_actor()
    ### --------------------------------------------
    
    # Test success behavior for the update_actor endpoint

    def test_update_actor_success(self):
        actor_id = 1
        updated_data = {
            'name': 'Updated Actor Name',
            'date_of_birth': '1995-05-05',
            'gender': 'Female'
        }
        response = self.client().patch(
            f'/actors/{actor_id}',
            json=updated_data,
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('edited_actor', data)

    # Test error behavior for the update_actor endpoint

    def test_update_actor_error(self):
        # Trying to update a non-existing actor
        actor_id = 999
        updated_data = {
            'name': 'Updated Actor Name',
            'date_of_birth': '1995-05-05',
            'gender': 'Female'
        }
        response = self.client().patch(
            f'/actors/{actor_id}',
            json=updated_data,
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: get_movies()
    ### --------------------------------------------

    # Test success behavior for the get_movies endpoint

    def test_get_movies_success(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {self.casting_assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    # Test error behavior for the get_movies endpoint

    def test_get_movies_error(self):
        response = self.client().get(
            '/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    ### --------------------------------------------
    ### Tests according to function: get_movie_detail()
    ### --------------------------------------------
    
    # Test success behavior for the get_movie_detail endpoint

    def test_get_movie_detail_success(self):
        # Assuming movie_id 1 exists in the database
        response = self.client().get(
            '/movies/1',
            headers={'Authorization': f'Bearer {self.casting_assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['movie'])

    # Test error behavior for the get_movie_detail endpoint

    def test_get_movie_detail_error(self):
        # Assuming movie_id 999 does not exist in the database
        response = self.client().get(
            '/movies/999',
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: delete_movie()
    ### --------------------------------------------
    
    # Test success behavior for the delete_actor endpoint

    def test_delete_movie_success(self):
        # Assuming movie_id 20 exists in the database
        response = self.client().delete(
            '/movies/20',
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_movie'], 20)

    # Test error behavior for the delete_movie endpoint

    def test_delete_movie_error(self):
        # Assuming casting assistant has no permissions to delete movies
        response = self.client().delete(
            '/movies/5',
            headers={'Authorization': f'Bearer {self.casting_assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: create_movie()
    ### --------------------------------------------
    
    # Test success behavior for the create_movie endpoint

    def test_create_movie_success(self):
        movie_data = {
            'title': 'Scarface',
            'release_date': 1983,
            'actors': ['Al Pacino']
        }
        response = self.client().post(
            '/movies',
            json=movie_data,
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('new_movie', data)

    # Test error behavior for the create_movie endpoint

    def test_create_movie_error(self):
        # Missing actor in database that is is given in the field in 'actors'
        movie_data = {
            'title': 'Django Unchained',
            'release data': 2012,
            'actors': ['Jamie Foxx']
        }
        response = self.client().post(
            '/movies',
            json=movie_data,
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
    
    ### --------------------------------------------
    ### Tests according to function: update_movie()
    ### --------------------------------------------
    
    # Test success behavior for the update_movie endpoint

    def test_update_movie_success(self):
        movie_id = 16
        updated_data = {
            "actors": ["Robert De Niro"]
        }
        response = self.client().patch(
            f'/movies/{movie_id}',
            json=updated_data,
            headers={'Authorization': f'Bearer {self.casting_director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('edited_movie', data)

    # Test error behavior for the update_movie endpoint

    def test_update_movie_error(self):
        # Trying to update a non-existing movie
        movie_id = 999
        updated_data = {
            'title': 'Updated Movie Name'
        }
        response = self.client().patch(
            f'/actors/{movie_id}',
            json=updated_data,
            headers={'Authorization': f'Bearer {self.executive_producer_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])



if __name__ == "__main__":
    unittest.main()