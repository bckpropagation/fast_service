from datetime import date
from app import db


class Reviews(db.Model):
    __tablename__ = 'reviews'

    rev_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(120), nullable=True)
    score = db.Column(db.Numeric, nullable=True)
    review = db.Column(db.Text, nullable=True)

    # Default values
    date_created = db.Column(db.Date, nullable=False, default=date.today)

    # Foreign keys
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, author: str, score: float, review: str, dish_id: int):
        self.author = author
        self.score = score
        self.review = review
        self.dish_id = dish_id

    def __repr__(self):
        return f'<Review {self.rev_id} on dish {self.dish_id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self.rev_id

    @staticmethod
    def get(dish_id):
        return Reviews.query.filter_by(dish_id=dish_id).all()
