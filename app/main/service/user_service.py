from typing import Dict, Tuple

from app.main import db
from app.main.model.user import User
from sqlalchemy.exc import IntegrityError


def get_user_by_public_id(public_id: str) -> Dict[str, str]:
	return User.query.filter_by(public_id=public_id).first_or_404()


def create_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
	try:
		usr = User(**data)
		save_changes(usr)

		response_object = {
			"status": "success", 
			"message": "User created",
			"public_id": usr.public_id
		}

		return response_object, 201
	
	except IntegrityError as integrityErr:
		return {
			"status": "fail",
			"message": "A user with that email is registered"
		}, 401


def save_changes(usr: User) -> None:
	db.session.add(usr)
	db.session.commit()
