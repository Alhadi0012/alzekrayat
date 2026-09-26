"""
Alzikrayat - Photo Sharing Application
Entry point of the application.
"""
from app import createApp
from app.config import Config

app = createApp()

if __name__ == "__main__":
    # Flask is used ONLY as an HTTP listener; all dispatching is done by our manual Router.
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
