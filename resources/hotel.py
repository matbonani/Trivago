from flask_restful import Resource, reqparse

from models.hotel import HotelModel


class Hoteis(Resource):

    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument("nome")
    arguments.add_argument("estrelas")
    arguments.add_argument("diaria")
    arguments.add_argument("cidade")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        # Verificando o retorno da função acima
        if hotel:
            return hotel.json()
        return {"Message": "Hotel not found."}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        dados = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()

        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.arguments.parse_args()

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:  # se o hotel existir vamos atualizar, caso contrário iremso criar
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201  # created

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found"}, 404

