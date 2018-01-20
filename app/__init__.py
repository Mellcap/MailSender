#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery
from flask_bootstrap import Bootstrap
from flask_admin import Admin

from config import config

# Flask extensions
db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__,
                broker=os.environ.get('CELERY_BROKER_URL', 'redis://'),
                backend=os.environ.get('CELERY_BACKEND_URL', 'redis://')
)
celery.config_from_object('celeryconfig')
bootstrap = Bootstrap()
admin = Admin(name='MailSender', template_mode='bootstrap3')


def create_app(config_name):
    '''
    Create app based on config name.
    The application factory, which takes as an argument the name\
    of a configuration to use for the application.
    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init extensions
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)

    # register blueprint
    from app.api import api as api_blueprint
    from app.form import form as form_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(form_blueprint, url_prefix='/forms')

    return app
