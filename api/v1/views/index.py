#!/usr/bin/python3
"""
defines routes for `app_views` blueprint
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """returns api status"""
    return jsonify(status="OK")
