#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from app.exceptions import ValidationError
from app.api import api

def bad_request(message):
    response = jsonify({'error': 'INVALID REQUEST', 'message': message, 'code': 400})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])