#!/usr/bin/env python3
"""
    New view for Session Authentication
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login/',
                 methods=['POST'],
                 strict_slashes=False)
@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login():
    """ Login route """
    from api.v1.app import auth
    email = request.form.get('email')
    pd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pd:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(pd):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response, 200


@app_views.route('/auth_session/logout/',
                 methods=['DELETE'],
                 strict_slashes=False)
@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ Delete Session """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
