#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

form = Blueprint('form', __name__)

from app.form import email_events, email_groups