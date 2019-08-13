import unittest
import json
import os

from app import create_app, db

from models.dish import Dishes
from models.review import Reviews


class ReviewsTestCase(unittest.TestCase):
	""" Test definitions for the Dishes object model """
	def fill_db(self):
		with open('tests/dishes_test_data.json') as jfile:
			for dish in json.load(jfile):
				db.session.add(Dishes(**dish))
			
			with open('tests/reviews_test_data.json') as jfile:
				for review in json.load(jfile):
					db.session.add(Reviews(**review))
			
			db.session.commit()

	def setUp(self):
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client

		with self.app.app_context():
			db.create_all()
			self.fill_db()

	def test_retrieve_single_dish_reviews(self):
		response = self.client().get('/dishes/1/reviews')
		json_data = json.loads(response.data)
		
		self.assertEqual(response.status_code, 200, '[!] Status code is not 200')
		self.assertGreater(len(json_data), 0, '[!] No data was returned.')
	
	def test_create_review(self):
		review = {
			"author": "ac nibh fusce lacus",
			"score": 3.29,
			"review": "Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui.\n\nMaecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam. Suspendisse potenti.",
			"dish_id": 1
		  }

		response = self.client().post('/dishes/1/reviews', data=review)
		self.assertEqual(response.status_code, 200, '[!] No data was returned.')
		self.assertIsNotNone(response.data, '[!] Review was not created.')

		response = self.client().get('/dishes/1/reviews')
		json_data = json.loads(response.data)
		self.assertEqual(len(json_data), 2, '[!] Review was not created.')

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