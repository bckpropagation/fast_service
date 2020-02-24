from flask_testing import TestCase
from manage import app

from app import url_prefix
from app.main import db


ENDPOINTS = {
	"user": f"{url_prefix}/user",
	"login": f"{url_prefix}/auth/login",
	"logout": f"{url_prefix}/auth/logout",
	"restaurants": f"{url_prefix}/restaurants"
}

class BaseTestCase(TestCase):
	def create_app(self):
		app.config.from_object("app.main.config.TestingConfig")
		return app
	
	def setUp(self):
		db.create_all()
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
