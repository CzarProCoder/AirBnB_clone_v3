#!/usr/bin/python3
"""
defines routes for places in `app_views` blueprint
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User

from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """retrieves all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves a place by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a new place for a given city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place = request.get_json()
    if not place:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in place:
        return jsonify(error="Missing user_id"), 400
    user = storage.get(User, place['user_id'])
    if not user:
        abort(404)
    if 'name' not in place:
        return jsonify(error="Missing name"), 400
    place = Place(**place)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        return jsonify(error="Not a JSON"), 400
    for key, value in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
