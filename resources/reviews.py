from flask_restful import Resource, reqparse, marshal, fields

from flask import abort

from models import review

class Date(fields.Raw):
    def format(self, date):
        return f'{date.day}/{date.month}/{date.year}'

reviews_type = {
            'rev_id': fields.Integer,
            'author': fields.String,
            'review': fields.String,
            'score': fields.Float,
            'date_of_review': Date,
        }


class Reviews(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('author',
                                    type=str,
                                    default='Anonymous',
                                    location='form')
        self.reqparser.add_argument('review',
                                    type=str,
                                    location='form',
                                    required=True)
        self.reqparser.add_argument('score',
                                    type=float,
                                    location='form')

        super(Reviews, self).__init__()

    def get(self, dish_id=None):
        if not dish_id:
            abort(400, description="Invalid request")

        dish_reviews = review.Reviews.get(dish_id)

        if dish_reviews:
            return marshal(dish_reviews, reviews_type)
        else:
            abort(404, description=f'There are no reviews for dish {dish_id}')

    def post(self, dish_id):
        self.args = self.reqparser.parse_args()
        return review.Reviews(self.args.author,
                              self.args.score,
                              self.args.review,
                              dish_id).save()

