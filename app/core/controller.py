"""Base controller shared by every controller in the Application Tier."""
from flask import render_template, redirect, session, flash
from app.models.user import User


class Controller:
    """Provides view rendering, redirection and session helpers."""

    @staticmethod
    def view(template, **context):
        """Render a Jinja template (output is auto-escaped against XSS)."""
        return render_template(template, **context)

    @staticmethod
    def redirectTo(path, message=None, category="success"):
        """Redirect the browser, optionally flashing a message first."""
        if message:
            flash(message, category)
        return redirect(path)

    @staticmethod
    def currentUser():
        """Return the logged-in user record, or None when there is no session."""
        userId = session.get("userId")
        return User.findById(userId) if userId else None

    @staticmethod
    def isLoggedIn():
        """True when an authenticated session exists."""
        return session.get("userId") is not None
