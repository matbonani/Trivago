from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.hotel import HotelModel


class Hoteis(Resource):

    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument("nome", type=str, required=True, help="The field 'nome' cannot be left blank")
    arguments.add_argument("estrelas", type=float, required=True, help="The field 'estrelas' cannot be left blank")
    arguments.add_argument("diaria", type=float, required=True, help="The field 'diarias' cannot be left blank")
    arguments.add_argument("cidade",  type=str, required=True, help="The field 'nome' cannot be left blank")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        # Verificando o retorno da função acima
        if hotel:
            return hotel.json()
        return {"Message": "Hotel not found."}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        dados = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel"}, 500
        return hotel.json(), 200

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.arguments.parse_args()

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:  # se o hotel existir vamos atualizar, caso contrário iremso criar
            hotel.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel"}, 500
            return hotel.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel"}, 500
        return hotel.json(), 201  # created

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel"}, 500
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found"}, 404

