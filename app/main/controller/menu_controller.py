import json

from flask_restplus import Resource
from typing import Dict, List


from ..utils.dto import MenuDto
from app.main.service.menu_service import (
	get_restaurant_menu,
	get_dish_information,
	get_dishes_by_type
)


api = MenuDto.api
_menu = MenuDto.menu
_dish = MenuDto.dish


@api.route("/<int:rest_id>/menu")
@api.param("rest_id", "Restaurant id")
class Menu(Resource):
	parser = api.parser()
	parser.add_argument(
		"type",
		type=str,
		location="args",
		choices=["lunch", "breakfast", "dinner", "vegan"],
		help="Valid menu choices"
	)

	@api.doc(
		"Restaurant menu information",
		responses={
			200: ("Success", _menu),
			404: "Not found"
		}
	)
	@api.marshal_list_with(_menu)
	@api.expect(parser)
	def get(self, rest_id):
		"""
		Returns the whole restaurant menu or filtered by type.
		"""
		args = self.parser.parse_args()

		if args.get("type"):
			return self.get_dish_by_type(rest_id, args.get("type"))

		return self.restaurant_menu(rest_id)

	def get_dish_by_type(self, rest_id: int, type: str) -> List[Dict[str, str]]:
		"""
		Return all restaurant dishes that are of a particular type.
		"""
		return get_dishes_by_type(rest_id, type)

	def restaurant_menu(self, rest_id: int) -> List[Dict[str, str]]:
		"""
		Returns restaurant menu.
		"""
		response = get_restaurant_menu(rest_id)

		if not response:
			api.abort(code=404, status="fail", description="Restaurant does not has menu")

		return response


@api.route("/<int:rest_id>/menu/<int:dish_id>")
@api.param("rest_id", "Restaurant id")
@api.param("dish_id", "Dish Id")
class Dish(Resource):
	@api.doc(
		"Dish information",
		responses={
			200: ("Success", _dish),
			404: ("Not found")
		}
	)
	@api.marshal_with(_dish, code=200)
	def get(self, rest_id, dish_id):
		"""
		Return a particular dish information.
		"""
		return get_dish_information(rest_id, dish_id)
