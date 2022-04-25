from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from models.user import UserModel


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"Message": "User not found."}, 404

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
            dados = arguments.parse_args()
            if UserModel.find_by_username(dados["username"]):
                return {"message": "The username '{}' alredy exists".format(dados["username"])}
            user = UserModel(**dados)
            try:
                user.save_user()
            except:
                return {"message": "An internal error ocurred trying to save hotel"}, 500
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
            access_token = create_access_token(identity=user.user_id)
            return {"accces_token": access_token}, 200
        return {"message": "The username or password is incorrect"}, 401
