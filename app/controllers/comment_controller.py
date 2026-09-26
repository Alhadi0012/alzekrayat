"""Stores comments written on a photo."""
from flask import request
from app.core.controller import Controller
from app.models.photo import Photo
from app.models.comment import Comment


class CommentController(Controller):
    """Handles the commenting engine of the photo detail view."""

    @staticmethod
    def store(id):
        """Attach a timestamped comment from the current user to photo {id}."""
        if not Controller.isLoggedIn():
            return Controller.redirectTo("/login", "Please login to comment.", "warning")
        if not Photo.findById(id):
            return "Photo Not Found", 404

        commentText = request.form.get("comment", "").strip()
        if not commentText:
            return Controller.redirectTo("/photo/%d" % id,
                                         "Comment cannot be empty.", "danger")

        Comment.create(id, Controller.currentUser()["id"], commentText)
        return Controller.redirectTo("/photo/%d" % id, "Comment added.")
