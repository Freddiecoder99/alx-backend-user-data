#!/usr/bin/env python3
"""
Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handles the login endpoint to authenticate a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
        print("User search result:", user)
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    session_name = getenv("SESSION_NAME")
    response = jsonify(user[0].to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """
    Handles the logout endpoint to delete a session.
    """
    from api.v1.app import auth
    res = auth.destroy_session(request)

    if not res:
        abort(404)

    return jsonify({}), 200
