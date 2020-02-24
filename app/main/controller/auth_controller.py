import json

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest


from ..utils.dto import AuthDto
from ..service.auth_service import Auth


api = AuthDto.api
_auth = AuthDto.auth
_login_resp = AuthDto.login_resp
_general_resp = AuthDto.general_resp


@api.route("/login")
class UserLogin(Resource):
	def validate_payload(self, func):
		try:
			super().validate_payload(func)

		except BadRequest as error:
			error.data["status"] = "fail"

			api.abort(400, **error.data)

	@api.doc(
		"Login service",
		responses={
			200: ("Success", _login_resp),
			401: ("Fail", _general_resp)
		}
	)
	@api.expect(_auth, validate=True)
	def post(self):
		"""
		Logs in a registered user.
		"""

		response = Auth.login(**api.payload)
		return response


@api.route("/logout")
class UserLogout(Resource):
	parser = api.parser()
	parser.add_argument(
		"Authorization",
		dest="auth_token",
		required=True,
		location="headers",
		help="Authorization token"
	)
	parser.add_argument(
		"user_id",
		dest="user_public_id",
		location="json",
		required=True,
		help="Public user id",
		nullable=False
	)

	@api.doc(
		"Logout service",
		responses={
			200: ("Successfully logged out", _general_resp),
			401: ("fail", _general_resp)
		}
	)
	@api.marshal_with(_general_resp)
	@api.expect(parser)
	def post(self):
		"""
		Ends user session.
		"""
		return Auth.logout(**self.parser.parse_args())
