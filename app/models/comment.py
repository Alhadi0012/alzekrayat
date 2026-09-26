"""Comment model: hand-written SQL for the comments table."""
from app.core.database import Database


class Comment:
    """Maps rows of the comments table, joined with their author."""

    @staticmethod
    def create(photoId, userId, commentText):
        """Insert a comment and return its generated id."""
        return Database.execute(
            "INSERT INTO comments (photo_id, user_id, comment) VALUES (%s, %s, %s)",
            (photoId, userId, commentText))

    @staticmethod
    def findByPhoto(photoId):
        """Return all comments of one photo, oldest first."""
        return Database.select(
            """SELECT c.*, u.first_name, u.last_name
               FROM comments c JOIN users u ON u.id = c.user_id
               WHERE c.photo_id = %s ORDER BY c.id ASC""", (photoId,))

    @staticmethod
    def countAll():
        """Return the total number of comments in the system."""
        return Database.selectOne("SELECT COUNT(*) AS total FROM comments")["total"]
