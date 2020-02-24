from .. import db
from ..model.blacklist import BlacklistToken


def blacklist_token(token):
	blacklist_token = BlacklistToken(token)

	db.session.add(blacklist_token)
	db.session.commit()
