import datetime
import jwt
import uuid

from flask.logging import logging
from flask_login import UserMixin

from app.main import db, bcrypt
from ..config import key


baseConfig = logging.basicConfig()


class User(UserMixin, db.Model):
	""" User model """
	__tablename__ = "users"

	# System fields
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	registered_on = db.Column(db.DateTime, nullable=False, default=False)
	public_id = db.Column(db.String(100), nullable=False, unique=True)

	# User fields
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(255), nullable=False, unique=True)
	passwd = db.Column(db.String(100), nullable=False)

	def __init__(
		self: "User",
		first_name: str,
		last_name: str,
		email: str,
		passwd: str
	) -> None:
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.passwd = bcrypt.generate_password_hash(passwd).decode("utf-8")

		self.public_id = str(uuid.uuid4())
		self.registered_on = datetime.datetime.utcnow()

	@property
	def password(self):
		raise AttributeError("password: Read-only field")

	def check_password(self, password: str) -> bool:
		return bcrypt.check_password_hash(self.passwd, password)
	
	def get_id(self):
		return self.public_id

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	@property
	def is_authenticated(self):
		return True

	def encode_auth_token(self, user_id):
		"""
		Generates the auth token.
		"""
		payload = {
			"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
			"iat": datetime.datetime.today(),
			"sub": user_id
		}

		return jwt.encode(payload, key, algorithm="HS256")

	@staticmethod
	def decode_auth_token(auth_token: str):
		return jwt.decode(auth_token, key).get("sub")
