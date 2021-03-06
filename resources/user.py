import traceback
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from flask import make_response, render_template

from models.user import UserModel
from blacklist import BLACKLIST


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"Message": "User not found."}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "An internal error ocurred trying to save hotel"}, 500
            return {"message": "User deleted."}
        return {"message": "User not found"}, 404


class UserRegister(Resource):

        def post(self):
            arguments = reqparse.RequestParser()
            arguments.add_argument("username", type=str, required=True, help="The field 'nome' cannot be left blank")
            arguments.add_argument("password", type=str, required=True, help="The field 'nome' cannot be left blank")
            arguments.add_argument("email", type=str)
            arguments.add_argument("activated", type=bool)

            dados = arguments.parse_args()
            if not dados.get('email') or dados.get('email') is None:
                return {"messatge": "The field 'email' cannot be left blank"}, 400

            if UserModel.find_by_email(dados['email']):
                return {"message": "The email '{}' is already exists".format(dados['email'])}, 400

            if UserModel.find_by_username(dados["username"]):
                return {"message": "The username '{}' alredy exists".format(dados["username"])}
            user = UserModel(**dados)
            user.activated = False  # garantido o False para esse campo
            try:
                user.save_user()
                user.send_confimation_email()
            except:
                user.delete_user()
                traceback.print_exc()
                return {"message": "An internal server error has ocurred"}, 500
            return {"message": "User created succesfully."}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        arguments = reqparse.RequestParser()
        arguments.add_argument("username", type=str, required=True, help="The field 'nome' cannot be left blank")
        arguments.add_argument("password", type=str, required=True, help="The field 'nome' cannot be left blank")
        dados = arguments.parse_args()

        user = UserModel.find_by_username(dados["username"])
        if user and safe_str_cmp(user.password, dados["password"]):
            if user.activated:
                access_token = create_access_token(identity=user.user_id)
                return {"accces_token": access_token}, 200
            return {"message": "User not confirmed"}, 400
        return {"message": "The username or password is incorrect"}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()["jti"]  # pega o token e envia para o BLACKLIST
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully"}, 200


class UserConfirm(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User id '{}' not found".format(user_id)}, 404
        user.activated = True
        user.save_user()
        # return {"message": "User id '{}' confirmed succesfuly".format(user_id)}, 200
        headers = {"Content-Tyope": "text/html"}  # informando o formato para enviar
        return make_response(render_template('user_confirm.html', email=user.email, username=user.username), 200, headers)