"""
Application factory.
Flask is used only as an HTTP listener: a single catch-all rule forwards
every request to the hand-written Router in app/routes.py.
"""
import os
from flask import Flask, request
from app.config import Config
from app.core.database import Database
from app.core.controller import Controller


def createApp():
    """Build and configure the Flask application object."""
    app = Flask(__name__,
                template_folder="views/templates",
                static_folder="static")
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

    from app.routes import router

    @app.route("/", defaults={"path": ""},
               methods=["GET", "POST"])
    @app.route("/<path:path>", methods=["GET", "POST"])
    def dispatch(path):
        """Single entry point: hand the request over to the manual Router."""
        return router.dispatch(request.method, "/" + path)

    @app.context_processor
    def injectCurrentUser():
        """Make the logged-in user available to every view (for the navbar)."""
        return {"currentUser": Controller.currentUser()}

    app.teardown_appcontext(Database.close)

    with app.app_context():
        Database.createSchema()

    return app
