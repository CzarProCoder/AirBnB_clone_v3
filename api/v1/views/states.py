#!/usr/bin/python3
"""
defines routes for states `app_views` blueprint
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State

from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves list of all states"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    state = request.get_json()
    if not state:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in state:
        return jsonify(error="Missing name"), 400
    state = State(**state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json()
    if not state_data:
        return jsonify(error="Not a JSON"), 400
    for key, value in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save
    return jsonify(state.to_dict()), 200
