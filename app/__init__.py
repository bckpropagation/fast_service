from flask_restplus import Api
from flask import Blueprint


from .main.controller.restaurants_controller import api as restaurants_ns
from .main.controller.menu_controller import api as menu_ns


__version__ = "v1"
blueprint = Blueprint("api", __name__)
api = Api(
	blueprint,
	version="1.0",
	title="Fast service API",
	description="Fast service API",
	catch_all_404s=True
)


api.add_namespace(restaurants_ns, path=f"/api/{__version__}")
api.add_namespace(menu_ns, path=f"/api/{__version__}/restaurants")
