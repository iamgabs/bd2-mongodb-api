## GABRIEL CARVALHO

# > API DISPONÍVEL ATÉ O DIA 02/12/2023

# link http://34.133.167.201/
# rotas => 
# cadastrar = /register
# pegar um usuário = /user=?username=
# pegar todos os usuários / users
# atualizar /user
# deletar /user/id

# exemplo de objeto:
# {
#     "name": "",
#     "age": 0,
#     "nacionality": "",
#     "username": "",
#     "password": ""
# }

import os
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import hashlib
from vars import *
from secret_keys import URI

app = Flask(__name__)

client = MongoClient(URI, server_api=ServerApi('1'))
print(OKGREEN, "Conexão estabelecida", ENDC)
db = client["my_database"]
collection = db["users"]

@app.route("/register", methods=["POST"])
def register():
    """
    Função é um endpoint para a API, que deve cadastrar um usuário
    Retorno: mensagem de confirmação ou erro
    """
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    nacionality = data["nacionality"]
    username = data["username"]
    password = data["password"]

    user = collection.find_one({"username": username})
    if user:
        return jsonify({"message": "User already exists"}), 400

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwdhash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    hashed_password = salt + pwdhash

    user = {"name": name, "age": age, "nacionality": nacionality, "username": username, "password": hashed_password}
    collection.insert_one(user)

    return jsonify({"message": "User created successfully"}), 201


@app.route("/user", methods=["GET"])
def get_user():
    """
    Função é um endpoint para a API, que deve um usuário
    Retorno: um usuário cujo username foi especificado
    """
    username = request.args.get("username")

    if not username:
        return jsonify({"message": "Username parameter is missing"}), 400

    user = collection.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found"}), 404

    user["_id"] = str(user["_id"])

    user.pop("password")
    return jsonify(user), 200


@app.route("/users", methods=["GET"])
def get_all_users():
    """
    Função é um endpoint para a API, que deve listar todos os usuários
    Retorno: lista de usuários ou mensagem em caso de nulo
    """
    users_cursor = collection.find({})

    users_list = list(users_cursor)
    for user in users_list:
        user.pop("password", None)
        user["_id"] = str(user["_id"])

    return jsonify(users_list), 200



@app.route("/user", methods=["PATCH"])
def update_user():
    """
    Função é um endpoint para a API, que deve atualizar um usuário
    Retorno: mensagem de confirmação ou erro
    """
    data = request.get_json()
    user_id = data["_id"]

    user = collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    name = data.get("name", user["name"])
    age = data.get("age", user["age"])
    nacionality = data.get("nacionality", user["nacionality"])
    username = data.get("username", user["username"])

    collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"name": name, 
                "age": age, 
                "nacionality": nacionality,
                "username": username
                }}
    )

    return jsonify({"message": "User updated successfully"}), 200


@app.route("/user/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Função é um endpoint para a API, que deve deletar um usuário
    Retorno: mensagem de confirmação ou erro
    """
    user = collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    collection.delete_one({"_id": ObjectId(user_id)})

    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
