import json
import os
import random
import unittest


from typing import List


from app import __version__
from app.main import db
from app.test.base import BaseTestCase
from app.main.model.restaurant import Restaurant


ENDPOINTS = {
	"rests": f"/api/{__version__}/restaurants",
	"single": f"/api/{__version__}/restaurants/1",
	"not_found": f"/api/{__version__}/restaurants/9999999"
}


def create_restaurants() -> None:
	rest = Restaurant("La Farola", "09:00-18:00")

	db.session.add(rest)
	db.session.commit()


class TestRestaurants(BaseTestCase):
	def test_retrieve_restaurants(self):
		create_restaurants()

		response = self.client.get(ENDPOINTS["rests"])

		self.assertEqual(response.status, "200 OK")

		for data in json.loads(response.data.decode()):
			self.assertNotEqual(data["id"], None)
			self.assertNotEqual(data["name"], None)
	
	def test_retrieve_restaurant_by_id(self):
		create_restaurants()

		response = self.client.get(ENDPOINTS["single"])

		self.assertEqual(response.status, "200 OK")

		data = json.loads(response.data.decode())
		self.assertEqual(data["id"], 1)
		self.assertEqual(data["name"], "La Farola")
	
	def test_throw_error_on_not_found(self):
		create_restaurants()

		response = self.client.get(ENDPOINTS["not_found"])
		self.assertEqual(response.status, "404 NOT FOUND")
