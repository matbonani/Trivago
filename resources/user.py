from flask_restful import Resource

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

