import json
import os
import random
import unittest


from typing import List


from app import __version__
from app.main import db
from app.test.base import BaseTestCase, ENDPOINTS
from app.main.model.restaurant import Restaurant
from app.main.model.menu import Menu


TYPES = ["lunch", "breakfast", "dinner", "vegan"]


def create_restaurants() -> None:
	rest = Restaurant("La Farola", "09:00-18:00")
	rest.menus = create_menus()
	db.session.add(rest)

	rest_2 = Restaurant("Restaurant no menu", "09:30-12:00")
	db.session.add(rest_2)
	db.session.commit()


def create_menus() -> List[Menu]:
	global TYPES

	return [
		Menu(
			f"Menu {_type}",
			_type,
			f"Desc {_type}",
			random.randrange(10, 300)
		)
		for _type in TYPES
	]


class TestMenu(BaseTestCase):
	def setUp(self):
		super().setUp()
		create_restaurants()

	def test_retrieve_restaurants_minified_menu_information(self):
		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/1")
			
			self.assertEqual(response.status_code, 200)

			data = json.loads(response.data.decode())
			self.assertIsNotNone(data.get("name"))
			self.assertIsNotNone(data.get("hours"))

			self.assertIsNotNone(data.get("menus"))

			for menu in data.get("menus"):
				self.assertIsNotNone(menu.get("id"))
				self.assertIsNotNone(menu.get("name"))
				self.assertIsNotNone(menu.get("type"))
				self.assertFalse("description" in menu)

	def test_retrieve_menus_from_one_restaurant(self):
		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/1/menu")

			self.assertEqual(response.status, "200 OK")
			
			data = json.loads(response.data.decode())

			self.assertTrue(isinstance(data, list))
			self.assertEqual(4, len(data))
	
	def test_return_error_on_empty_menu(self):
		create_restaurants()
		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/2/menu")
			self.assertEqual(response.status_code, 404)

	def test_return_dish_information(self):

		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/1/menu/1")

			self.assertEqual(response.status_code, 200)

			data = json.loads(response.data.decode())
			self.assertIsNotNone(data.get("name"))
			self.assertIsNotNone(data.get("type"))
			self.assertIsNotNone(data.get("description"))
	
	def test_get_dishes_by_type(self):
		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/1/menu?type=lunch")

			self.assertEqual(response.status_code, 200)
			self.assertIsNotNone(response.json)

	def test_return_error_on_retrieving_non_existing_type(self):
		with self.app.test_client() as client:
			response = client.get(f"{ENDPOINTS.get('restaurants')}/1/menu?type=lun")

			self.assertEqual(response.status_code, 400)

			errors = response.json.get("errors", None)
			self.assertIsNotNone(errors)
			self.assertEqual(
				errors.get("type"),
				"Valid menu choices The value 'lun' is not a valid choice for 'type'."
			)

if __name__ == "__main__":
	unittest.main()
