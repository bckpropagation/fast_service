from fast_service import db


class Token(db.Model):
    __tablename__ = 'tokens'

    token_id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    token = db.Column()
