#!/usr/bin/env python3
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users():
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id):
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        user = request.current_user
    else:
        user = User.get(user_id)
        if not user:
            abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    rj = request.get_json()
    if not rj or rj.get("email") == "" or rj.get("password") == "":
        return jsonify({'error': "Wrong format"}), 400
    user = User()
    user.email = rj.get("email")
    user.password = rj.get("password")
    user.first_name = rj.get("first_name")
    user.last_name = rj.get("last_name")
    user.save()
    return jsonify(user.to_json()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    rj = request.get_json()
    if not rj:
        return jsonify({'error': "Wrong format"}), 400
    if 'first_name' in rj:
        user.first_name = rj['first_name']
    if 'last_name' in rj:
        user.last_name = rj['last_name']
    user.save()
    return jsonify(user.to_json()), 200
