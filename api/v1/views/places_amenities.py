#!/usr/bin/python3
"""
defines routes for places amenities in `app_views` blueprint
"""

from flask import abort, jsonify
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place

from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """retrieves all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == "db":
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, _id) for _id in place.amenity_ids]
    return jsonify([amenity.to_dict() for amenity in amenities])
