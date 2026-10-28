from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from jwt import jwt_required

class Hoteis(Resource):
    @jwt_required()
    def get(self):
        return { "hoteis": [hotel.json() for hotel in HotelModel.query.all()] }

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="Nome obrigatório")
    argumentos.add_argument("estrelas", type=float, required=True, help="Estrelas obrigatório")
    argumentos.add_argument("diaria", type=float, required=True, help="Diária obrigatório")
    argumentos.add_argument("cidade", type=str, required=True, help="Cidade obrigatório")
   
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return { "message": "Hotel not found" }, 404
   
   @jwt_required()
    def post(self,hotel_id):
        dados = Hotel.argumentos.parse_args() # Dicionário
        if Hotel.find_hotel(hotel_id):
            return { "message": "Hotel with this id already exists"}
        try:
            novo_hotel = HotelModel(hotel_id, **dados)
            novo_hotel.save_hotel()
        except:
            return { "message": "An internal error ocurred trying to save hotel."}, 500
   
   @jwt_required()
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args() # Dicionário
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.update_hotel(dados["nome"], dados["estrelas"], dados["diaria"], dados["cidade"])
                hotel.save_hotel()
                return hotel.json(), 200
            except:
                return { "message": "An internal error ocurred trying to update hotel."}, 500
        try:
            novo_hotel = HotelModel(hotel_id, **dados)
            novo_hotel.save_hotel()
            return novo_hotel.json(), 201
        except FileNotFoundError:
            return { "message": "An internal error ocurred trying to create hotel."}, 500

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {"message": "Hotel deleted"}, 200
            except:
                return { "message": "An internal error ocurred trying to delete hotel."}, 500
        return { "message": "Hotel not found."}, 404