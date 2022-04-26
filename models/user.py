from db import db
from flask import request, url_for
from requests import post


MAILGUN_DOMAIN = '#'
MAILGUN_API_KEY = '#'
FROM_TITLE = 'No-Reply'
FROM_EMAIL = 'no-reply@restapi.com'


class UserModel(db.Model):
    __tablename__ = 'user'

    # definindo as colunas do banco
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, activated):
        self.username = username
        self.password = password
        self.email = email
        self.activated = activated

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "activated": self.activated
        }

    def send_confimation_email(self):
        #     http://127.0.0.1:5000  + /confirm/user_id
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                          'to': self.email,
                          'subject': 'Confirmação de email',
                          'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                          'html': '<html><p>\
                          Confirme seu cadasto clicando no link a seguir <a href="{}">Confirma Email</a>\
                          </p></html>'.format(link)
                          }
                    )

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

    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()  # SELECT * FROM hoteis WHERE hotel_id=hotel_id
        if email:
            return email
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()