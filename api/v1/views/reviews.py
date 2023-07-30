#!/usr/bin/python3
"""
defines routes for reviews in `app_views` blueprint
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """retrieves all reviews for a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrieves a review by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review for a given place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review = request.get_json()
    if not review:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in review:
        return jsonify(error="Missing user_id"), 400
    user = storage.get(User, review['user_id'])
    if not user:
        abort(404)
    if 'text' not in review:
        return jsonify(error="Missing text"), 400
    review = Review(**review)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        return jsonify(error="Not a JSON"), 400
    for key, value in review_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save
    return jsonify(review.to_dict()), 200
