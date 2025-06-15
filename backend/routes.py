from . import app
import os
import json
from flask import jsonify, request,redirect, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200

######################################################################
# COUNT PICTURES
######################################################################
@app.route("/count")
def count():
    return jsonify({"length": len(data)}), 200

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET SPECIFIC PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        picture = next((item for item in data if item.get("id") == id), None)
        if picture:
            return jsonify(picture), 200
        return jsonify({"message": "Picture not found"}), 404
    except Exception:
        return jsonify({"message": "Internal server error"}), 500


######################################################################
# CREATE PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    
    if not new_picture or "id" not in new_picture:
        return jsonify({"message": "Invalid input"}), 400
    
    existing = next((item for item in data if item["id"] == new_picture["id"]), None)
    if existing:
        response = make_response(
            jsonify({"Message": f"picture with id {new_picture['id']} already present"}),
            302  # Status code expected by test
        )
        response.headers['Location'] = url_for('get_picture_by_id', id=new_picture["id"])
        return response
    
    data.append(new_picture)
    return jsonify(new_picture), 201






######################################################################
# UPDATE PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_data = request.get_json()
    picture = next((item for item in data if item["id"] == id), None)
    
    if not picture:
        return jsonify({"message": "Picture not found"}), 404
        
    picture.update(update_data)
    return jsonify(picture), 200

######################################################################
# DELETE PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    original_count = len(data)
    data = [item for item in data if item["id"] != id]
    
    if len(data) == original_count:
        return jsonify({"message": "Picture not found"}), 404
    
    return "", 204

