"""Landing page and static About Us page."""
from app.core.controller import Controller
from app.models.user import User
from app.models.photo import Photo
from app.models.comment import Comment


class HomeController(Controller):
    """Serves the welcome page with live statistics."""

    @staticmethod
    def index():
        """Show the landing page: hero, statistics and the latest photos."""
        statistics = {"users": User.countAll(),
                      "photos": Photo.countAll(),
                      "comments": Comment.countAll()}
        return Controller.view("home.html",
                               statistics=statistics,
                               latestPhotos=Photo.all()[:6])

    @staticmethod
    def about():
        """Show the static About Us description of Alzikrayat."""
        return Controller.view("about.html")
