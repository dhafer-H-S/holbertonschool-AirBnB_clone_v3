#!/usr/bin/python3
"""Review object that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get reviews for all object of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get review  for specified place"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response()(jsonify(({}), 200))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        abort(400, description="Missing user_id")
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    if 'text' not in kwargs:
        abort(400, description="Missing text")
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()

    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
