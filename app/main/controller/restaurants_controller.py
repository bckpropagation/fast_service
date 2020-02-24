from flask import request
from flask_restplus import Resource


from ..utils.dto import RestaurantsDto
from app.main.service.restaurants_service import get_all_restaurants, get_restaurant_by_id


api = RestaurantsDto.api
_restaurant = RestaurantsDto.restaurant
_resp = RestaurantsDto.general_resp


@api.route("")
class RestaurantList(Resource):

	@api.doc(
		"Information of registered restaurants.",
		responses={
			200: ("Success", _restaurant),
			204: ("NO CONTENT")
		}
	)
	@api.marshal_list_with(_restaurant, code=200, mask="id, name, hours")
	def get(self):
		"""
		Returns a list of all registered restaurants.
		"""
		return get_all_restaurants()


@api.route("/<int:id>")
@api.param("id", "Restaurant id number")
class Restaurant(Resource):

	@api.doc(
		"Retrieve restaurant by id",
		responses={
			200: ("Success", _restaurant),
			404: ("Restaurant not found")
		}
	)
	@api.marshal_with(_restaurant)
	def get(self, id):
		"""
		Retrieve restaurant by it's id
		"""
		return get_restaurant_by_id(id)
