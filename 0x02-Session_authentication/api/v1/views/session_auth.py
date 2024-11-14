#!/usr/bin/env python3
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if not session_id:
        abort(500)

    response = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)
    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

