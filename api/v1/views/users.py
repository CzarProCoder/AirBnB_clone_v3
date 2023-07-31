#!/usr/bin/python3
"""
defines routes for users in `app_views` blueprint
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User

from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """retrieves all users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """retrieves a user by their id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user by their id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a new user"""
    user = request.get_json()
    if not user:
        return jsonify(error="Not a JSON"), 400
    if 'email' not in user:
        return jsonify(error="Missing email"), 400
    if 'password' not in user:
        return jsonify(error="Missing password"), 400
    user = User(**user)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a user by their id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        return jsonify(error="Not a JSON"), 400
    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
