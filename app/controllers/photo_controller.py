"""Photo gallery, detail view, upload and ownership-checked deletion."""
import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from app.core.controller import Controller
from app.models.photo import Photo
from app.models.comment import Comment
from app.config import Config


class PhotoController(Controller):
    """Implements the CRUD operations of the Photos entity."""

    @staticmethod
    def index():
        """Show the gallery. ?style=grid3 | grid4 | list changes the layout."""
        return Controller.view("photos/index.html",
                               photos=Photo.all(),
                               style=request.args.get("style", "grid3"))

    @staticmethod
    def show(id):
        """Show one photo in detail with its metadata and comments."""
        photo = Photo.findById(id)
        if not photo:
            return "Photo Not Found", 404
        return Controller.view("photos/show.html",
                               photo=photo, comments=Comment.findByPhoto(id))

    @staticmethod
    def create():
        """Display the upload form (authorized users only)."""
        if not Controller.isLoggedIn():
            return Controller.redirectTo("/login", "Please login first.", "warning")
        return Controller.view("photos/create.html")

    @staticmethod
    def store():
        """Save the uploaded file on disk and its metadata in the database."""
        if not Controller.isLoggedIn():
            return Controller.redirectTo("/login", "Please login first.", "warning")

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        uploadedFile = request.files.get("photo")

        errors = Photo.validate(title, uploadedFile.filename if uploadedFile else "",
                                Config.ALLOWED_EXTENSIONS)
        if errors:
            return Controller.view("photos/create.html", errors=errors)

        # A random name prevents overwriting and path-traversal through the file name.
        extension = secure_filename(uploadedFile.filename).rsplit(".", 1)[1].lower()
        storedName = "photo_%s.%s" % (uuid.uuid4().hex, extension)
        os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
        uploadedFile.save(os.path.join(Config.UPLOAD_DIR, storedName))

        Photo.create(Controller.currentUser()["id"], storedName, title, description)
        return Controller.redirectTo("/photos", "Photo uploaded successfully.")

    @staticmethod
    def delete(id):
        """Delete a photo after verifying that it belongs to the current user."""
        if not Controller.isLoggedIn():
            return Controller.redirectTo("/login", "Please login first.", "warning")

        photo = Photo.findById(id)
        if not photo:
            return "Photo Not Found", 404
        if photo["user_id"] != Controller.currentUser()["id"]:
            return Controller.redirectTo("/photos",
                                         "You can only delete your own photos.", "danger")

        filePath = os.path.join(Config.UPLOAD_DIR, photo["file_name"])
        if os.path.exists(filePath):
            os.remove(filePath)          # keep the disk in sync with the database
        Photo.delete(id)
        return Controller.redirectTo("/photos", "Photo deleted.")
