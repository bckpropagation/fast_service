from flask import request
from flask_restplus import Resource


from ..utils.dto import MenuDto
from app.main.service.menu_service import get_restaurant_menu, get_dish_information

api = MenuDto.api
_menu = MenuDto.menu
_dish = MenuDto.dish


@api.route("/<int:rest_id>/menu")
@api.param("rest_id", "Restaurant id")
@api.response(204, "No menu")
class Menu(Resource):

	@api.doc("Restaurant menu information")
	@api.marshal_list_with(_menu)
	def get(self, rest_id):
		response = get_restaurant_menu(rest_id)

		if response:
			return response

		return [], 204


@api.route("/<int:rest_id>/menu/<int:id>")
@api.param("rest_id", "Restaurant id")
@api.param("id", "Dish id")
@api.response(404, "Menu not found")
class Dish(Resource):

	@api.doc("Dish information")
	@api.marshal_with(_dish)
	def get(self, rest_id, id):
		return get_dish_information(rest_id, id)
