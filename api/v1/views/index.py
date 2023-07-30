#!/usr/bin/python3
"""
defines routes for `app_views` blueprint
"""

from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """returns api status"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """returns resource statistics"""
    resources = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    stats = {}
    for key, value in resources.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
