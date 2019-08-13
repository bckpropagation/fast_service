from sqlalchemy.dialects.postgresql import JSON

from app import db


class Dishes(db.Model):
    __tablename__ = 'dishes'

    dish_id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    dish_type = db.Column(db.String(15), nullable=False)
    ingredients = db.Column(JSON, nullable=False)

    # Relationship(s)
    dish_review = db.relationship('Reviews',
                                  passive_deletes=True,
                                  backref='dishes',
                                  lazy='dynamic')

    def __init__(self, name: str, price: float, dish_type: str, ingredients: dict):
        self.name = name
        self.price = price
        self.dish_type = dish_type
        self.ingredients = ingredients

    def __repr__(self):
        return f'<Dish {self.dish_id} type {self.dish_type}>'

    @staticmethod
    def get_all():
        return Dishes.query.all()

    @staticmethod
    def get_by_id(dish_id):
        return Dishes.query.get(dish_id)

    @staticmethod
    def get_by_type(dish_type):
        return Dishes.query.filter_by(dish_type=dish_type).all()

