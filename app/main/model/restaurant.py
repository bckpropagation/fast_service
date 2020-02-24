from .. import db


class Restaurant(db.Model):
	""" Restaurant information model """
	__tablename__ = "restaurant"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	hours = db.Column(db.String(30), nullable=False)
	menus = db.relationship(
		"Menu",
		cascade="save-update, delete, delete-orphan",
		lazy="select",
		backref=db.backref("restaurant", lazy="joined")
	)

	def __init__(self, rest_name, hours):
		self.name = rest_name
		self.hours = hours
	
	def __repr__(self):
		return f"<id: {self.id} name: {self.name}>"
