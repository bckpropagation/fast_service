import datetime


from app.main import db


class BlacklistToken(db.Model):
	__tablename__ = "blacklisted_tokens"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	token = db.Column(db.String(500), nullable=False, unique=True)
	blacklisted_on = db.Column(db.DateTime, nullable=False)

	def __init__(self, token):
		self.token = token
		self.blacklisted_on = datetime.datetime.utcnow()

	@staticmethod
	def is_token_blacklisted(token):
		return bool(BlacklistToken.query.filter_by(token=token).first())
