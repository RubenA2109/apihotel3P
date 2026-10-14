from flask_restful import Resource

lista_hoteis = [
    {"hotel_id": "sky","nome": "Hotel sky", "estrelas": 4.8, "diaria": 195.99, "cidade": "Porto"},
    {"hotel_id": "sky1","nome": "Hotel sky1", "estrelas": 4.8, "diaria": 195.99, "cidade": "Porto"},
    {"hotel_id": "sky2","nome": "Hotel sky2", "estrelas": 4.8, "diaria": 195.99, "cidade": "Porto"}
]

class Hoteis(Resource):
    def get(self):
        return {"hoteis": lista_hoteis}