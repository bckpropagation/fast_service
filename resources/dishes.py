from flask import abort
from flask_restful import Resource, fields, marshal, reqparse

from models import dish

dish_fields = {
                'dish_id': fields.Integer,
                'name': fields.String,
                'price': fields.Price(decimals=2),
                'ingredients': fields.Raw
              }


class Dishes(Resource):
    def get(self, dish_id=None, dish_type=None):
        if dish_id:
            return self.get_dish(dish_id)
        elif dish_type:
            return self.get_dishes_by_type(dish_type)
        else:
            return self.get_all_dishes()

    def get_all_dishes(self):
        menu = dish.Dishes.get_all()
        if menu:
            return marshal(menu, dish_fields), 200
        else:
            abort(404, description="No data")

    def get_dish(self, dish_id):
        dish_desc = dish.Dishes.get_by_id(dish_id)

        if dish_desc:
            return marshal(dish_desc, dish_fields), 200
        else:
            abort(404, description='Dish not found')

    def get_dishes_by_type(self, dish_type):
        dishes_by_type = dish.Dishes.get_by_type(dish_type)

        if dishes_by_type:
            return marshal(dishes_by_type, dish_fields)
        else:
            abort(404, description=f'Type not found')
