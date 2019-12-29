from app.main import db
from app.main.model.restaurant import Restaurant


def get_all_restaurants():
	return Restaurant.query.all()


def get_restaurant_by_id(id):
	return Restaurant.query.filter_by(id=id).first_or_404(
		description=f"There is no restaurant for id {id}"
	)
