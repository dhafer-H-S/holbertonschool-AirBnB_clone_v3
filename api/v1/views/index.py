#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage
DicText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """stats"""
    return_dict = {}
    for key, value in DicText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


if __name__ == "__main__":
    pass
