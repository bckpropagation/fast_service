from .. import db


class Menu(db.Model):
	""" Menu information model """
	__tablename__ = "menu"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	type = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	price = db.Column(db.Float, nullable=False, server_default="0.0")
	restaurant_id = db.Column(
		db.Integer,
		db.ForeignKey("restaurant.id"),
		nullable=False
	)

	def __init__(self, name, type, description, price, restaurant_id=None):
		self.name = name
		self.type = type
		self.description = description
		self.price = price

		if restaurant_id:
			self.restaurant_id = restaurant_id

	def __repr__(self):
		return f"<Name: {self.name} Price: {self.price}>"
