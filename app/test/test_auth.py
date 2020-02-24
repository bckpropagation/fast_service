import json
import unittest


from app.main import db
from app.test.base import BaseTestCase, ENDPOINTS
from app.main.model.user import User
from app.main.model.blacklist import BlacklistToken
from app.test.test_user import register_new_user


def success_login(client):
	user_data = {
		"email": "new@example.com",
		"passwd": "test_password"
	}
	return client.post(
		ENDPOINTS.get("login"),
		data=json.dumps(user_data),
		content_type="application/json"
	)


def incorrect_login(client):
	user_data = {
		"email": "test@example.com",
		"passwd": "test_password"
	}
	return client.post(
		ENDPOINTS.get("login"),
		data=json.dumps(user_data),
		content_type="application/json"
	)


def erroneous_login(client):
	user_data = {
		"user": "err_user",
		"passwd": "test_password"
	}

	return client.post(
		ENDPOINTS.get("login"),
		data=json.dumps(user_data),
		content_type="application/json"
	)


class AuthenticationTest(BaseTestCase):
	def setUp(self):
		super().setUp()
		register_new_user(self)

	def test_successful_login(self):
		with self.app.test_client() as client:
			response = success_login(client)

			self.assertEqual(200, response.status_code)
			self.assertEqual("success", response.json.get("status"))
			self.assertIsNotNone(response.json.get("Authorization"))

	def test_incorrect_password(self):
		with self.app.test_client() as client:
			response = incorrect_login(client)

			self.assertEqual(response.status_code, 401)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual("Email or password is incorrect", response.json.get("message"))
	
	def test_try_to_login_with_non_existent_user(self):
		with self.app.test_client() as client:
			response = incorrect_login(client)

			self.assertEqual(response.status_code, 401)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual("Email or password is incorrect", response.json.get("message"))

	def test_retrieve_error_on_invalid_parameters(self):
		with self.app.test_client() as client:
			response = erroneous_login(client)

			self.assertEqual(response.status_code, 400)
			self.assertEqual("Input payload validation failed", response.json.get("message"))
			self.assertEqual("fail", response.json.get("status"))

			errors = response.json.get("errors")
			self.assertEqual("'email' is a required property", errors.get("email"))

	def test_logout(self):
		with self.app.test_client() as client:
			response = success_login(client)

			self.assertEqual(200, response.status_code)
			self.assertEqual("success", response.json.get("status"))

			auth_token = response.json.get("Authorization")
			user_public_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				headers={
					"Authorization": f"Bearer {auth_token}"
				},
				data=json.dumps(
					{
						"user_id": user_public_id
					}
				),
				content_type="application/json"
			)
			self.assertEqual(200, response.status_code)
			self.assertEqual("success", response.json.get("status"))

	def test_check_if_token_was_blacklisted(self):
		with self.app.test_client() as client:
			response = success_login(client)

			self.assertEqual(200, response.status_code)
			self.assertEqual("success", response.json.get("status"))

			auth_token = response.json.get("Authorization")
			user_public_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				data=json.dumps(
					{
						"user_id": user_public_id
					}
				),
				headers={
					"Authorization": f"Bearer {auth_token}"
				},
				content_type="application/json"
			)

			self.assertEqual(200, response.status_code)
			self.assertEqual("success", response.json.get("status"))

			self.assertTrue(BlacklistToken.is_token_blacklisted(auth_token))

	def test_try_to_logout_using_a_different_user_id(self):
		response = self.client.post(
			ENDPOINTS.get("user"),
			data = json.dumps(
				{
					"first_name": "new",
					"last_name": "user",
					"email": "test@example.com",
					"passwd": "test_password",
				}
			),
			content_type="application/json"
		)

		user_2 = response.json.get("public_id")
		with self.app.test_client() as client:
			response = success_login(client)
			auth_token = response.json.get("Authorization")
			user_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				content_type="application/json",
				headers={
					"Authorization": f"Bearer {auth_token}"
				},
				data=json.dumps(
					{
						"user_id": user_2
					}
				)
			)

			self.assertEqual(401, response.status_code)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual(
				"Invalid issuer",
				response.json.get("message")
			)

	def test_try_to_logout_with_an_invalid_token(self):
		with self.app.test_client() as client:
			response = success_login(client)
			auth_token = response.json.get("Authorization")
			user_public_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				data=json.dumps(
					{
						"user_id": user_public_id
					}
				),
				headers={
					"Authorization": f"Bearer {auth_token[1:]}"
				},
				content_type="application/json"
			)

			self.assertEqual(401, response.status_code)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual("Invalid token", response.json.get("message"))

	def test_try_to_logout_using_a_null_token(self):
		with self.app.test_client() as client:
			response = success_login(client)
			auth_token = response.json.get("Authorization")
			user_public_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				data=json.dumps(
					{
						"user_id": user_public_id
					}
				),
				headers={
					"Authorization": f"Bearer {None}"
				},
				content_type="application/json"
			)

			self.assertEqual(401, response.status_code)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual("Invalid token", response.json.get("message"))

	def test_try_to_logout_without_a_bearer_token(self):
		with self.app.test_client() as client:
			response = success_login(client)
			auth_token = response.json.get("Authorization")
			user_public_id = User.decode_auth_token(auth_token)

			response = client.post(
				ENDPOINTS.get("logout"),
				data=json.dumps(
					{
						"user_id": user_public_id
					}
				),
				headers={
					"Authorization": f"test"
				},
				content_type="application/json"
			)

			self.assertEqual(401, response.status_code)
			self.assertEqual("fail", response.json.get("status"))
			self.assertEqual("Invalid token", response.json.get("message"))


if __name__ == "__main__":
	unittest.main()
