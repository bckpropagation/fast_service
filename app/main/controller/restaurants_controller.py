from flask import request
from flask_restplus import Resource


from ..utils.dto import RestaurantsDto
from app.main.service.restaurants_service import get_all_restaurants, get_restaurant_by_id


api = RestaurantsDto.api
_min_restaurant = RestaurantsDto.minified_restaurant
_restaurant = RestaurantsDto.restaurant


@api.route("/restaurants")
@api.response(204, "No restaurants")
class RestaurantList(Resource):

	@api.doc("Information of registered restaurants.")
	@api.marshal_list_with(_min_restaurant)
	def get(self):
		return get_all_restaurants()


@api.route("/restaurants/<int:id>")
@api.param("id", "Restaurant id number")
class Restaurant(Resource):

	@api.doc("Retrieve restaurant by id")
	@api.marshal_with(_restaurant)
	@api.response(404, "Restaurant not found")
	def get(self, id):
		return get_restaurant_by_id(id)
