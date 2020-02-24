import json
import os
import random
import unittest


from typing import List

from app.main import db
from app.test.base import BaseTestCase, ENDPOINTS
from app.main.model.restaurant import Restaurant


def create_restaurants() -> None:
	rest = Restaurant("La Farola", "09:00-18:00")

	db.session.add(rest)
	db.session.commit()


class TestRestaurants(BaseTestCase):
	def setUp(self):
		super().setUp()
		create_restaurants()

	def test_retrieve_restaurants(self):
		response = self.client.get(ENDPOINTS.get("restaurants"))

		self.assertEqual(response.status, "200 OK")

		for data in json.loads(response.data.decode()):
			self.assertNotEqual(data["id"], None)
			self.assertNotEqual(data["name"], None)
	
	def test_retrieve_restaurant_by_id(self):
		response = self.client.get(f"{ENDPOINTS.get('restaurants')}/1")

		self.assertEqual(response.status, "200 OK")

		data = json.loads(response.data.decode())
		self.assertEqual(data["name"], "La Farola")
		self.assertEqual(data["hours"], "09:00-18:00")
	
	def test_throw_error_on_not_found(self):
		response = self.client.get(f"{ENDPOINTS.get('restaurants')}/9999999")
		self.assertEqual(response.status, "404 NOT FOUND")

	def test_get_204_no_restaurants_code(self):
		Restaurant.query.filter_by(id=1).delete()

		response = self.client.get(f"{ENDPOINTS.get('restaurants')}")
		self.assertEqual(response.status, "204 NO CONTENT")
