from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import sqlite3

from models.hotel import HotelModel
from models.site import SiteModel
from resources.filters import normalize_path_params, consulta_com_cidade, consulta_sem_cidade


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
            "hotel_id": linha[0],
            "nome": linha[1],
            "estrelas": linha[2],
            "diaria": linha[3],
            "cidade": linha[4],
            "site_id": linha[5]

            })
        connection.close()
        return {"hoteis": hoteis}
        # return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument("nome", type=str, required=True, help="The field 'nome' cannot be left blank")
    arguments.add_argument("estrelas", type=float, required=True, help="The field 'estrelas' cannot be left blank")
    arguments.add_argument("diaria", type=float, required=True, help="The field 'diarias' cannot be left blank")
    arguments.add_argument("cidade",  type=str, required=True, help="The field 'cidade' cannot be left blank")
    arguments.add_argument("site_id",  type=int, required=True, help="Every hotel needs to be linked with a site")

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

        # verificando existencia de site
        if not SiteModel.find_by_id(dados['site_id']):
            return {"message": "The hotel must be associated to a valid site id. "}, 400

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

