from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


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

    # initialize the plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # include the main routes
        from .user_management.user_management import user_bp
        from .homepage.homepage import home_bp
        from .text_checker.text_checker import text_bp
        from .labeling.labeling import label_bp
        from .data_importer.data_importer import data_in_bp

        # register blueprints
        app.register_blueprint(user_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(text_bp)
        app.register_blueprint(label_bp)
        app.register_blueprint(data_in_bp, url_prefix="/data_importer")

        db.drop_all()

        # we create the db once
        db.create_all()

        return app