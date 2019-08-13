import json
import os
import unittest

from app import create_app, db

from models.dish import Dishes


class DishesTestCase(unittest.TestCase):
	""" Test definitions for the Dishes object model """
	def fill_db(self):
		with open('tests/dishes_test_data.json') as jfile:
			for dish in json.load(jfile):
				db.session.add(Dishes(**dish))
			
			db.session.commit()

	def setUp(self):
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client

		with self.app.app_context():
			db.create_all()
			self.fill_db()

	def test_retrieve_all_dishes(self):
		response = self.client().get('/dishes/')
		json_data = json.loads(response.data)

		self.assertEqual(response.status_code, 200, '[!] Status code not 200.')
		self.assertGreater(len(response.data), 0, '[!] No data returned.')

	def test_retrieve_one_dish(self):
		response = self.client().get('/dishes/1')
		json_data = json.loads(response.data)

		self.assertEqual(response.status_code, 200, '[!] Status code not 200.')
		self.assertEqual(json_data['dish_id'], 1,
						 '[!] Retrieved dish id is different.')

	def test_retrieve_dishes_by_type(self):
		response = self.client().get('/dishes/desayuno')
		json_data = json.loads(response.data)

		self.assertEqual(response.status_code, 200, '[!] Status code not 200.')
		self.assertGreater(len(json_data), 0,
						   '[!] No data was returned.')

	def test_get_error_on_non_existent_dish(self):
		response = self.client().get('/dishes/10000000')
		json_data = json.loads(response.data)

		self.assertEqual(response.status_code, 404, '[!] Status code not 404.')
		self.assertEqual(json_data['message'], 'Dish not found',
						 '[!] Response is different.')
	
	def test_get_error_on_non_existent_dish_type(self):
		response = self.client().get('/dishes/qwerty')
		json_data = json.loads(response.data)

		self.assertEqual(response.status_code, 404, '[!] Status code not 404.')
		self.assertEqual(json_data['message'], 'Type not found',
						 '[!] Response is different.')

	def tearDown(self):
		""" Teardown all initialized data """
		with self.app.app_context():
			db.session.remove()
			
			# Reviews depends on dishes.
			from models.review import Reviews
			Reviews.__table__.drop(db.engine)
			Dishes.__table__.drop(db.engine)


if __name__ == "__main__":
	unittest.main()
