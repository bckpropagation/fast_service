import json
import os
import unittest


from app import __version__
from app.main import db
from app.test.base import BaseTestCase, ENDPOINTS
from app.main.model.user import User


def create_user() -> None:
	usr = User("test", "user", "test@example.com", "123456")

	db.session.add(usr)
	db.session.commit()

	return usr.public_id


def register_new_user(self):
	return self.client.post(
		ENDPOINTS.get("user"),
		data = json.dumps(
			{
				"first_name": "new",
				"last_name": "user",
				"email": "new@example.com",
				"passwd": "test_password",
			}
		),
		content_type="application/json"
	)


class UserTest(BaseTestCase):

	def test_get_user_by_public_id(self):
		public_id = create_user()

		response = self.client.get(f"{ ENDPOINTS.get('user') }/{ public_id }")

		self.assertTrue(response.status_code == 200)

		self.assertEqual(public_id, response.json.get("public_id"))
		self.assertEqual("test", response.json.get("first_name"))
		self.assertEqual("user", response.json.get("last_name"))

		self.assertFalse("passwd" in response.json)
	
	def test_get_error_on_non_existent_user_public_id(self):
		response = self.client.get(f"{ENDPOINTS.get('user')}/user/deadbeef")
		self.assertTrue(response.status_code == 404)

	def test_create_new_user(self):
		with self.client:
			response = register_new_user(self)
			self.assertEqual(response.status_code, 201)

	def test_throw_error_on_creating_user_with_existing_email(self):		
		with self.client:
			response = register_new_user(self)
			self.assertEqual(response.status_code, 201)

			response = register_new_user(self)
			self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
	unittest.main()
