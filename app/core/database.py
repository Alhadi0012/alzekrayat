"""
Data Tier: a thin, hand-written database access layer.
No ORM is used - every statement is raw, parameterized SQL.
"""
from flask import g
from app.config import Config

MYSQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    location VARCHAR(100),
    description TEXT,
    occupation VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    photo_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

SQLITE_SCHEMA = MYSQL_SCHEMA.replace("INT AUTO_INCREMENT PRIMARY KEY",
                                     "INTEGER PRIMARY KEY AUTOINCREMENT")


class Database:
    """Opens one connection per request and runs hand-written SQL."""

    @staticmethod
    def connection():
        """Return the connection bound to the current request (opened once)."""
        if "dbConnection" not in g:
            if Config.DB_DRIVER == "mysql":
                import pymysql
                g.dbConnection = pymysql.connect(
                    host=Config.DB_HOST, user=Config.DB_USER,
                    password=Config.DB_PASSWORD, database=Config.DB_NAME,
                    charset="utf8mb4", autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor)
            else:
                import sqlite3
                g.dbConnection = sqlite3.connect(Config.SQLITE_PATH)
                g.dbConnection.row_factory = sqlite3.Row
                g.dbConnection.execute("PRAGMA foreign_keys = ON")
        return g.dbConnection

    @staticmethod
    def _sql(statement):
        """Adapt the %s placeholder style to the active driver."""
        return statement if Config.DB_DRIVER == "mysql" else statement.replace("%s", "?")

    @staticmethod
    def select(statement, parameters=()):
        """Run a SELECT and return a list of dictionaries."""
        cursor = Database.connection().cursor()
        cursor.execute(Database._sql(statement), parameters)
        rows = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in rows]

    @staticmethod
    def selectOne(statement, parameters=()):
        """Run a SELECT and return the first row, or None."""
        rows = Database.select(statement, parameters)
        return rows[0] if rows else None

    @staticmethod
    def execute(statement, parameters=()):
        """Run an INSERT/UPDATE/DELETE and return the new row id."""
        connection = Database.connection()
        cursor = connection.cursor()
        cursor.execute(Database._sql(statement), parameters)
        connection.commit()
        newId = cursor.lastrowid
        cursor.close()
        return newId

    @staticmethod
    def createSchema():
        """Create the three tables if they do not exist yet."""
        connection = Database.connection()
        schema = MYSQL_SCHEMA if Config.DB_DRIVER == "mysql" else SQLITE_SCHEMA
        for statement in [s.strip() for s in schema.split(";") if s.strip()]:
            cursor = connection.cursor()
            cursor.execute(statement)
            cursor.close()
        connection.commit()

    @staticmethod
    def close(_exception=None):
        """Close the request connection (registered as a teardown handler)."""
        connection = g.pop("dbConnection", None)
        if connection is not None:
            connection.close()
