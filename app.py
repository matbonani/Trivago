from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'         # criando um banco de dados na raiz
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLE'] = True                            # ativamos a lista negra
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_banco():
    db.create_all()


@jwt.token_in_blocklist_loader                        # verificamos se está na BLACKLIST
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader                             # se estiver na BLACKLIST, retorna a menssagem abaixo
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({"message": "You have been logged out"}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserConfirm, '/confirm/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
