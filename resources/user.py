from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

class user(Resource):
    def get(self, username):
        user = UserModel.find_user(username)
        if user:
            return user.json(), 200
        return { "message": "User not found" }, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {"message": "User deleted"}, 200
            except:
                return { "message": "An internal error occurred trying to delete user."}, 500
        return { "message": "User not found."}, 404

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="Username obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatório")

    def post(self):
        dados = UserRegister.argumentos.parse_args() # Dicionário
        if UserModel.find_user(dados["username"]):
            return { "message": "User with this username already exists"}
        try:
            novo_user = UserModel(**dados)
            novo_user.save_user()
            return { "message": "User created successfully."}, 201
        except:
            return { "message": "An internal error occurred trying to save user."}, 500

class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="Username obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatório")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])
        if user and compare_digest(user.password, dados["password"]):
            token_de_acesso = create_access_token(identity=user.id)
            return { "access_token": token_de_acesso }, 200
        return { "message": "Invalid username or password" }, 401

class userLogout(Resource):
    @jwt_required()
    def post(self):
        return { "message": "User logged out successfully."}, 200