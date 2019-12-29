import json
import os
import random
import unittest


from typing import List


from app import __version__
from app.main import db
from app.test.base import BaseTestCase
from app.main.model.restaurant import Restaurant
from app.main.model.menu import Menu


TYPES = ["lunch", "breakfast", "dinner", "vegan"]
random.seed(8888)


def create_restaurants() -> None:
	rest = Restaurant("La Farola", "09:00-18:00")
	rest.menus = create_menus(4)
	db.session.add(rest)

	rest_2 = Restaurant("Restaurant no menu", "09:30-12:00")
	db.session.add(rest_2)
	db.session.commit()


def create_menus(amount_of_menus: int) -> List[Menu]:
	global TYPES

	return [
		Menu(
			f"Menu No {random.random()}",
			random.choice(TYPES),
			f"Desc {random.random()}"
		)
		for idx in range(0, amount_of_menus)
	]


class TestMenu(BaseTestCase):
	def setUp(self):
		super().setUp()
		create_restaurants()

	def test_retrieve_restaurants_minified_menu_information(self):
		response = self.client.get("/api/v1/restaurants/1")
		
		self.assertTrue(response.status_code == 200)

		data = json.loads(response.data.decode())
		self.assertIsNotNone(data["id"])
		self.assertIsNotNone(data["name"])
		self.assertIsNotNone(data["hours"])

		self.assertIsNotNone(data["menus"])

		for menu in data["menus"]:
			self.assertIsNotNone(menu["id"])
			self.assertIsNotNone(menu["name"])
			self.assertIsNotNone(menu["type"])

	def test_retrieve_menus_from_one_restaurant(self):
		response = self.client.get("/api/v1/restaurants/1/menu")

		self.assertEqual(response.status, "200 OK")
		
		data = json.loads(response.data.decode())

		self.assertTrue(isinstance(data, list))
		self.assertEqual(4, len(data))
	
	def test_return_error_on_empty_menu(self):
		create_restaurants()
		response = self.client.get("/api/v1/restaurants/2/menu")

		self.assertTrue(response.status_code == 204)

	def test_return_dish_information(self):
		response = self.client.get("/api/v1/restaurants/1/menu?id=1")

		self.assertTrue(response.status_code == 200)

		data = json.loads(response.data.decode())
		self.assertIsNotNone(data["id"])
		self.assertIsNotNone(data["name"])
		self.assertIsNotNone(data["type"])
		self.assertIsNotNone(data["description"])
	
	def test_get_dishes_by_type(self):
		response = self.client.get("/api/v1/restaurants/1/menu?type=lunch")

		self.assertTrue(response.status_code == 200)
		self.assertIsNotNone(response.json)

	def test_return_error_on_retrieving_non_existing_type(self):
		response = self.client.get("/api/v1/restaurants/1/menu?type=lun")

		self.assertTrue(response.status_code == 400)

		errors = response.json.get("errors", None)
		self.assertIsNotNone(errors)
		self.assertEqual(
			errors.get("type"),
			"Dish types The value 'lun' is not a valid choice for 'type'."
		)

if __name__ == "__main__":
	unittest.main()
