#!/usr/bin/python3

"""app to connect to api"""

import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_appcontext(code):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(
        host=os.getenv(
            'HBNB_API_HOST', '0.0.0.0'), port=int(
            os.getenv(
                'HBNB_API_PORT', '5000')), threaded=True)
