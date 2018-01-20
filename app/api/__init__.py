#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import email_events, email_groups, errors