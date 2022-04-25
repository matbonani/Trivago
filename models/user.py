from db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    # definindo as colunas do banco
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()  # SELECT * FROM hoteis WHERE hotel_id=hotel_id
        if user:
            return user
        return None

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()  # SELECT * FROM hoteis WHERE hotel_id=hotel_id
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
