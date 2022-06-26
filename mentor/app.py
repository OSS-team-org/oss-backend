# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from mentor import commands, account
from mentor.account.views import blueprint as account_blueprint
from mentor.exceptions import InvalidUsage
from mentor.extensions import bcrypt, cache, db, migrate, cors
from mentor.settings import ProdConfig
from flask_mail import Mail
from flask_dance.contrib.github import make_github_blueprint, github
import os
# from flask_restplus import Api, Resource, fields

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
SECRET_KEY = os.environ.get("SECRET_KEY")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
mail = Mail()

def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(account_blueprint, origins=origins)
    app.config["SECRET_KEY"]=SECRET_KEY 

    github_blueprint = make_github_blueprint(client_id=GITHUB_CLIENT_ID,
                                         client_secret=GITHUB_CLIENT_SECRET)

    app.register_blueprint(github_blueprint, url_prefix='/github_login')
    
    # cors.init_app(benefit.views.blueprint,origins=origins)

    app.register_blueprint(account_blueprint)
    


def register_errorhandlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'Account': account.models.Account,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
