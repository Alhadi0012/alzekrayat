"""Authentication: registration, session login/logout and the last-login cookie."""
from datetime import datetime, timedelta
from flask import request, session, make_response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.controller import Controller
from app.models.user import User
from app.config import Config


class AuthController(Controller):
    """Handles all session state of the application."""

    @staticmethod
    def showRegister():
        """Display the registration form."""
        return Controller.view("auth/register.html")

    @staticmethod
    def register():
        """Validate the form, hash the password and create the account."""
        formData = {key: request.form.get(key, "").strip() for key in
                    ("firstName", "lastName", "email", "password",
                     "location", "description", "occupation")}
        errors = User.validate(formData)
        if User.findByEmail(formData["email"]):
            errors.append("This email address is already registered.")
        if errors:
            return Controller.view("auth/register.html", errors=errors, old=formData)

        # Passwords are stored as a PBKDF2 hash and can never be read back.
        userId = User.create(formData["firstName"], formData["lastName"],
                             formData["email"], generate_password_hash(formData["password"]),
                             formData["location"], formData["description"],
                             formData["occupation"])
        session["userId"] = userId
        return Controller.redirectTo("/photos", "Welcome to Alzikrayat!")

    @staticmethod
    def showLogin():
        """Display the login form together with the last-login cookie value."""
        return Controller.view("auth/login.html",
                               lastLogin=request.cookies.get(Config.LAST_LOGIN_COOKIE))

    @staticmethod
    def login():
        """Verify credentials, open the session and refresh the 7-day cookie."""
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.findByEmail(email)

        if not user or not check_password_hash(user["password"], password):
            return Controller.view("auth/login.html",
                                   errors=["Invalid email or password."],
                                   lastLogin=request.cookies.get(Config.LAST_LOGIN_COOKIE))

        session["userId"] = user["id"]
        response = make_response(redirect("/photos"))
        response.set_cookie(Config.LAST_LOGIN_COOKIE,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            expires=datetime.now() + timedelta(days=Config.LAST_LOGIN_COOKIE_DAYS),
                            httponly=True, samesite="Lax")
        return response

    @staticmethod
    def logout():
        """Destroy the session (the last-login cookie intentionally survives)."""
        session.clear()
        return Controller.redirectTo("/", "You have been logged out.")
