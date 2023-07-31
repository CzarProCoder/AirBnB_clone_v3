#!/usr/bin/python3
"""
defines routes for amenities in `app_views` blueprint
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity

from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """retrieves all amenities"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a new amenity"""
    amenity = request.get_json()
    if not amenity:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in amenity:
        return jsonify(error="Missing name"), 400
    amenity = Amenity(**amenity)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        return jsonify(error="Not a JSON"), 400
    for key, value in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
