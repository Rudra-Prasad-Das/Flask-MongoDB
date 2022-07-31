# from crypt import methods
import json
import mimetypes
from urllib import request, response
from flask import Flask,Response,request
from pymongo import MongoClient
from bson.objectid import ObjectId

app=Flask(__name__)

try:
   mongo=MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
   mongo.server_info() 
   db=mongo.company
except:
    print("ERR Cannot connect to db")
@app.route("/users",methods=["GET"])
def get_some_users():
    try:
        data=list(db.users.find())
        # print(data)
        for user in data:
            user["_id"]=str(user["_id"])
        return Response (
            response=json.dumps(data),
            status=500,
            mimetype="application/json" 
      )
    except Exception as ex:
        print(ex)
        return Response (
            response=json.dumps({"Message":"user cannot be read"}),
            status=500,
            mimetype="application/json" 
      )
@app.route("/users",methods=["POST"])
def create_user():
    try:
        user={"name":request.form["name"],"lastname":request.form["lastName"]}
        dbResponse=db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response (
            response=json.dumps({"message":"user created","id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
        
    except Exception as ex:
        print(ex)
@app.route("/users/<id>",methods=["PATCH"])
def update_user(id):
    try:
        dbResponse=db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        print(request.form["name"])
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        # return id
        return Response (
            response=json.dumps({"message":"user updated"}),
            status=200,
            mimetype="application/json"
        )
          
    except Exception as ex:
        print(ex)
        return Response (
            response=json.dumps({"Message":"user cannot be updated"}),
            status=500,
            mimetype="application/json" 
      )
@app.route("/users/<id>",methods=["DELETE"])
def user_delete(id):
    try:
        dbResponse=db.users.delete_one(
            {"_id":ObjectId(id)}
        )
        return Response (
            response=json.dumps({"Message":"user deleted"}),
            status=200,
            mimetype="application/json" 
      )
    except Exception as ex:
        print(ex)
        return Response (
            response=json.dumps({"Message":"user cannot be delted"}),
            status=500,
            mimetype="application/json" 
      )
          
    
if __name__=="__main__":
    app.run(port=80,debug=True)