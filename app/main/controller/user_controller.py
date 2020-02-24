from flask import request
from flask_restplus import Resource
from typing import Dict

from ..utils.dto import UserDto
from ..service.user_service import (
	get_user_by_public_id,
	create_user
)


api = UserDto.api

_user = UserDto.user_info
_new_user = UserDto.new_user
_login_resp = UserDto.login_resp
_fail_resp = UserDto.fail_resp



@api.route("/<string:public_id>")
@api.param("public_id", "User id")
class SingleUser(Resource):
	@api.doc("Get user information")
	@api.marshal_with(_user)
	def get(self, public_id: str) -> Dict[str, str]:
		"""
		Returns a user information.
		"""
		return get_user_by_public_id(public_id)


@api.route("")
class NewUser(Resource):
	@api.doc(
		"Register new user",
		responses={
			201: ("User created", _login_resp),
			401: ("User exists", _fail_resp)
		}
	)
	@api.expect(_new_user, validate=True)
	def post(self) -> Dict[str, str]:
		"""
		Register a new user.
		"""
		response_object = create_user(data=request.json)
		return response_object
