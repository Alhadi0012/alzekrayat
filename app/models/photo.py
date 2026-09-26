"""Photo model: hand-written SQL for the photos table."""
from app.core.database import Database


class Photo:
    """Maps rows of the photos table, joined with their author when needed."""

    @staticmethod
    def create(userId, fileName, title, description):
        """Insert photo metadata and return its generated id."""
        return Database.execute(
            """INSERT INTO photos (user_id, file_name, title, description)
               VALUES (%s, %s, %s, %s)""",
            (userId, fileName, title, description))

    @staticmethod
    def all():
        """Return every photo with its author name, newest first."""
        return Database.select(
            """SELECT p.*, u.first_name, u.last_name
               FROM photos p JOIN users u ON u.id = p.user_id
               ORDER BY p.id DESC""")

    @staticmethod
    def findById(photoId):
        """Return a single photo with its author, or None."""
        return Database.selectOne(
            """SELECT p.*, u.first_name, u.last_name
               FROM photos p JOIN users u ON u.id = p.user_id
               WHERE p.id = %s""", (photoId,))

    @staticmethod
    def findByUser(userId):
        """Return all photos that belong to one user."""
        return Database.select(
            "SELECT * FROM photos WHERE user_id = %s ORDER BY id DESC", (userId,))

    @staticmethod
    def delete(photoId):
        """Delete a photo row (comments are removed by ON DELETE CASCADE)."""
        Database.execute("DELETE FROM photos WHERE id = %s", (photoId,))

    @staticmethod
    def countAll():
        """Return the total number of uploaded photos."""
        return Database.selectOne("SELECT COUNT(*) AS total FROM photos")["total"]

    @staticmethod
    def validate(title, fileName, allowedExtensions):
        """Server-side validation for the upload form. Returns error messages."""
        errors = []
        if not title.strip() or len(title) > 200:
            errors.append("Title is required and must be 200 characters or fewer.")
        if "." not in fileName or fileName.rsplit(".", 1)[1].lower() not in allowedExtensions:
            errors.append("Only PNG, JPG, JPEG, GIF or WEBP images are allowed.")
        return errors
