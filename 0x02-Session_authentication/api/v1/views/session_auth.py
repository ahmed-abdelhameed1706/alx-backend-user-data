#!/usr/bin/env python3
"""session auth view"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
    "/auth_session/login/", methods=["POST"], strict_slashes=False
)  # no pep8
def login():
    """login method"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(users[0].id)

    response = make_response(jsonify(users[0].to_json()))

    response.set_cookie(getenv("SESSION_NAME"), session_id)

    return response


@app_views.route(
    "/auth_session/logout/", methods=["DELETE"], strict_slashes=False
)  # no pep8
def logout():
    """logout method"""
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
