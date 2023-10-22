import os

from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

MONGO_HOST = os.environ.get("MONGO_HOST")

client = MongoClient(MONGO_HOST, 27017)
db = client["test"]
collection = db["data"]


class Items(Resource):
    """A resource for managing objects in a MongoDB database.

    This resource supports the following HTTP methods:

    * GET: Returns the value of the object with the specified key.
    * POST: Creates a new object.
    * PUT: Updates the value of the object with the specified key.
    """

    @staticmethod
    @app.route("/<key>", methods=["GET"])
    def get(key: str) -> Response:
        """Returns the value of the object with the specified key.

        Args:
            key: The key of the object to get the value of.

        Returns:
            The value of the object with the specified key, or `None` if the object does not exist.
        """

        data = collection.find_one({"key": key})
        if not data:
            response = jsonify({"message": "Object not found"})
            response.status_code = 404
            return response

        response = jsonify({"value": data["value"]})
        response.status_code = 200
        return response

    @staticmethod
    @app.route("/", methods=["POST"])
    def post() -> Response:
        """Creates a new object.

        This method expects a JSON object in the request body with the following key:

        * `key`: The key of the new object.
        * `value`: The value of the new object.

        Returns:
            The key of the new object.
        """

        data = request.get_json()
        key = data["key"]
        value = data["value"]

        if collection.find_one({"key": key}):
            response = jsonify({"message": "Object with key `{}` already exists.".format(key)})
            response.status_code = 409
            return response

        # Create the new object
        collection.insert_one({"key": key, "value": value})
        message = "Object created successfully."
        response = jsonify({"message": message})
        response.status_code = 201
        return response

    @staticmethod
    @app.route("/<key>", methods=["PUT"])
    def put(key: str) -> Response:
        """Updates the value of the object with the specified key.

        If the object does not exist, creates a new object with the specified key and value.

        This method expects a JSON object in the request body with the following key:

        * `value`: The new value of the object with the specified key.

        Returns:
            The key of the object with the specified key.
        """

        data = request.get_json()
        collection.update_one({"key": key}, {"$set": {"value": data["value"]}}, upsert=True)
        response = jsonify({"key": key, "message": "Object created or updated successfully"})
        response.status_code = 200
        return response


api.add_resource(Items, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
