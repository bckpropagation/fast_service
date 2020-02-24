from app.main import db
from app.main.model.menu import Menu


def get_restaurant_menu(rest_id: int):
	result = Menu.query.filter_by(restaurant_id=rest_id).all()
	return result


def get_dish_information(rest_id: int, dish_id: int):
	result = Menu.query.filter_by(restaurant_id=rest_id, id=dish_id).first_or_404()
	return result


def get_dishes_by_type(rest_id: int, type: str):
	result = Menu.query.filter(
		Menu.type == type, Menu.restaurant_id == rest_id
	).all()
	return result
