# this will create a message board utilizing the following concept: application factory, blueprint, view functions (navigation menu)
# reference: https://realpython.com/flask-project/#leverage-blueprints
from flask import Flask
import os
from . import posts, pages, errors
from dotenv import load_dotenv # load .env file
from flask_sqlalchemy import SQLAlchemy
from .extensions import db
import logging
from .dash_app import create_dash_app
# from . import models  # Import models here to avoid circular import


# load .env file
load_dotenv()

# this function is "application factory", allows to flexibility and scaling
def create_app():

    # start the flask instance
    app = Flask(__name__)

    # enabling the use of environment variables, assess to all variables with "Flask_"
    app.config.from_prefixed_env()

    # get Flask from Environment
    app.config["ENVIRONMENT"] = os.getenv("ENVIRONMENT")

    # get Database from Environment, must be defined before db.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    # initiate database
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist

    # register blueprints, must be after initiating the database and creating the tables
    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)
    app.register_error_handler(404, errors.page_not_found)

    # setup Dash app
    create_dash_app(app)  # this mounts the Dash app at /dash/

    # adding logging to receive information about the server
    #print(f"Current Environment: {os.getenv('ENVIRONMENT')}") # method for getting variable that doesnt start with "FLASK_"
    #print(f"Using Database: {app.config.get('DATABASE')}") # method for getting variable that starts with "FLASK_"
    app.logger.debug(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    app.logger.debug(f"Using Database: {os.getenv('SQLALCHEMY_DATABASE_URI')}")

    return app





