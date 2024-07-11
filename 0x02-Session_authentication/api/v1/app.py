#!/usr/bin/env python3
"""
Main module for the API
"""

import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth based on AUTH_TYPE environment variable
auth_type = getenv('AUTH_TYPE', 'default')
if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """ Before request handler """
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

