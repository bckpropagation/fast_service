from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()
api = Api(catch_all_404s=True)


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')

	# Inits
	db.init_app(app)
	api.init_app(app)

	return app

############
## Routes ##
############
from resources.reviews import Reviews
from resources.dishes import Dishes

api.add_resource(Dishes, '/dishes',
                         '/dishes/',
                         '/dishes/<string:dish_type>',
                         '/dishes/<string:dish_type>/',
                         '/dishes/<int:dish_id>',
                         '/dishes/<int:dish_id>/',
                         endpoint='dishes')

api.add_resource(Reviews, '/dishes/<int:dish_id>/reviews',
                          '/dishes/<int:dish_id>/reviews/',
						  endpoint='reviews')

print(f'[*] Registered resources: {len(api.resources)}')