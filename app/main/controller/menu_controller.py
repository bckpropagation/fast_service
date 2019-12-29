import json

from flask_restplus import Resource

from ..utils.dto import MenuDto
from app.main.service.menu_service import (
	get_restaurant_menu,
	get_dish_information,
	get_dishes_by_type
)


api = MenuDto.api
_menu = MenuDto.menu
_dish = MenuDto.dish

parser = api.parser()
parser.add_argument(
	"id",
	type=int,
	location="args",
	help="Dish id number"
)
parser.add_argument(
	"type",
	type=str,
	location="args",
	choices=["lunch", "breakfast", "dinner", "vegan"],
	help="Dish types"
)


@api.route("/<int:rest_id>/menu")
@api.param("rest_id", "Restaurant id")
class Menu(Resource):
	@api.doc("Restaurant menu information")
	@api.response(200, "Success", _menu)
	@api.doc(
		responses = {
			204: "No menu",
			404: "Menu not found"
		}
	)
	@api.marshal_list_with(_dish)
	@api.expect(parser)
	def get(self, rest_id):
		response = None
		args = parser.parse_args()

		if args.get("id"):
			response = get_dish_information(
				rest_id,
				args.get("id")
			)
		elif args.get("type"):
			response = get_dishes_by_type(
				rest_id,
				args.get("type")
			)
		else:
			response = get_restaurant_menu(rest_id)

		if response:
			return response

		return [], 204
