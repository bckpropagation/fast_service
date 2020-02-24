import jwt

from flask_restplus import abort
from flask_login import current_user, login_user, logout_user

from ..service.blacklist_service import blacklist_token
from ..model.user import User


class Auth:
	@staticmethod
	def login(email: str, passwd: str):
		if current_user.is_authenticated:
			return

		user = User.query.filter_by(email=email).first()

		if user and user.check_password(passwd):
			auth_token = user.encode_auth_token(user.public_id)
			login_user(user)

			if auth_token:
				success_response = {
					"status": "success",
					"message": "Successfully logged in",
					"Authorization": auth_token.decode()
				}

				return success_response, 200
		else:
			fail_response = {
				"status": "fail",
				"message": "Email or password is incorrect"
			}
			return fail_response, 401

	@staticmethod
	def logout(auth_token: str, user_public_id: str):
		try:
			if not auth_token.startswith("Bearer"):
				raise jwt.InvalidTokenError()
			
			auth_token = auth_token[7:]
			sub = User.decode_auth_token(auth_token)

			if sub != user_public_id:
				raise jwt.InvalidIssuer()

			blacklist_token(auth_token)

			return {
				"status": "success",
				"message": "Successfully logged out"
			}, 200

		except jwt.InvalidIssuer as issuerError:
			abort(401, status="fail", message="Invalid issuer")

		except jwt.InvalidSignatureError as signatureError:
			abort(401, status="fail", message="Invalid signature")

		except jwt.ExpiredSignatureError as expiredError:
			abort(401, status="fail", message="Token expired")
		
		except jwt.InvalidTokenError as invalidToken:
			abort(401, status="fail", message="Invalid token")

