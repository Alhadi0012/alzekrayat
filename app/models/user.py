"""User model: hand-written SQL for the users table plus server-side validation."""
import re
from app.core.database import Database


class User:
    """Maps rows of the users table to plain dictionaries."""

    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
    NAME_PATTERN = re.compile(r"^[A-Za-z\u0600-\u06FF ]{2,50}$")

    @staticmethod
    def create(firstName, lastName, email, passwordHash, location, description, occupation):
        """Insert a new user and return its generated id."""
        return Database.execute(
            """INSERT INTO users (first_name, last_name, email, password,
                                  location, description, occupation)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (firstName, lastName, email, passwordHash, location, description, occupation))

    @staticmethod
    def findById(userId):
        """Return one user by primary key, or None."""
        return Database.selectOne("SELECT * FROM users WHERE id = %s", (userId,))

    @staticmethod
    def findByEmail(email):
        """Return one user by email address, or None."""
        return Database.selectOne("SELECT * FROM users WHERE email = %s", (email,))

    @staticmethod
    def countAll():
        """Return the total number of registered users."""
        return Database.selectOne("SELECT COUNT(*) AS total FROM users")["total"]

    @staticmethod
    def validate(formData):
        """Server-side validation layer. Returns a list of error messages."""
        errors = []
        if not User.NAME_PATTERN.match(formData.get("firstName", "").strip()):
            errors.append("First name is required (letters only, 2-50 characters).")
        if not User.NAME_PATTERN.match(formData.get("lastName", "").strip()):
            errors.append("Last name is required (letters only, 2-50 characters).")
        if not User.EMAIL_PATTERN.match(formData.get("email", "").strip()):
            errors.append("A valid email address is required.")
        if len(formData.get("password", "")) < 6:
            errors.append("Password must be at least 6 characters long.")
        return errors
