from flask import Flask
from flask_restful import Resource, Api

from resources.hotel import Hoteis, Hotel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'         # criando um banco de dados na raiz
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_banco():
    db.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
