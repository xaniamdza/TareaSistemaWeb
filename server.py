from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
from app import create_app

app = create_app()


try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR - No se puede conectar a DB")

@app.route("/login", methods = ["GET"])
def get_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(response = json.dumps(data), status = 200, mimetype = "aplication/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Error - no se puede leer usuarios"}), status = 500, mimetype = "aplication/json")


@app.route("/login", methods = ["POST"])
def create_user():
    try:
        user = {"username":request.form["username"], "password":request.form["password"]}
        dbResponse = db.users.insert_one(user)
        return Response(response = json.dumps({"message":"Usuario registrado", "id": f"{dbResponse.inserted_id}" }), status = 200, mimetype = "aplication/json") 
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Error - No se pudo registrar el usuario"}), status = 500, mimetype = "aplication/json")


@app.route("/login/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one({"_id":ObjectId(id)},{"$set":{"username":request.form["username"], "password":request.form["password"]}})
        for attr in dir(dbResponse):
            print(attr)
        return Response(response = json.dumps({"message":"Usuario actualizado"}), status = 200, mimetype = "aplication/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Error - No se actualizó"}), status = 500, mimetype = "aplication/json") 

@app.route("/login/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        for attr in dir(dbResponse):
            print(attr)
        return Response(response = json.dumps({"message":"Usuario Eliminado"}), status = 200, mimetype = "aplication/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Error - No se eliminó"}), status = 500, mimetype = "aplication/json")


if __name__ == "__main__":
    app.run(port=80, debug=True)