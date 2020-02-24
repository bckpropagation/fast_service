import os
from flask_restplus import Api
from flask import Blueprint

from .main import init
from .main.controller.restaurants_controller import api as restaurants_ns
from .main.controller.menu_controller import api as menu_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns


__version__ = "v1"
url_prefix = f"/api/{__version__}"
blueprint = Blueprint(
	"restaurants_api",
	__name__
)
api = Api(
	blueprint,
	version="1.0",
	title="Fast service API",
	doc="/api/doc",
	catch_all_404s=True,
	description="Fast service API<style>.models {display: none !important}</style>",
)


api.add_namespace(restaurants_ns, path=f"{url_prefix}/restaurants")
api.add_namespace(menu_ns, path=f"{url_prefix}/restaurants")
api.add_namespace(auth_ns, path=f"{url_prefix}/auth")
api.add_namespace(user_ns, path=f"{url_prefix}/user")

def create_app(config_name):
	app = init(config_name)

	with app.app_context():
		app.register_blueprint(blueprint)
	
	return app
