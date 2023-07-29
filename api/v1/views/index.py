#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def app_views():
    return jsonify(status="OK")
