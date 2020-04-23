from flask import Flask
from config import Config

def create_app():

    # create the base app object
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    with app.app_context():
        # include the main routes


        # register blueprints