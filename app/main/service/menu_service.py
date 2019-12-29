from app.main import db
from app.main.model.menu import Menu


def get_restaurant_menu(rest_id):
	return Menu.query.filter(Menu.restaurant_id == rest_id).all()


def get_dish_information(rest_id, id):
	return Menu.query.filter_by(restaurant_id=rest_id, id=id).first_or_404()


def get_dishes_by_type(rest_id, type):
	return Menu.query.filter(
		Menu.type == type, Menu.restaurant_id == rest_id
	).all()
