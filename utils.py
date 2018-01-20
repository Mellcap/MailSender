#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
import arrow

from app.exceptions import ValidationError

# Constant
# message
SUCCESS_MESSAGE = {"error": "", "message": "OK"}
SUCCESS_GET_MESSAGE = {"code": 200, "error": "", "message": "OK"}
SUCCESS_CREATE_MESSAGE = {"code": 201, "error": "", "message": "CREATED"}
NOT_FOUND_MESSAGE = {"code": 404, "error": "NOT FOUND", "message": "NOT FOUND"}
# time
DEFAULT_TIMEZONE = 'Asia/Singapore'
TIME_FORMAT = "DD MMM YYYY HH:mm"

VALIDERROR_TEMPLATE = {
    "wrong_type": "Wrong <%s> type, expect a %s.",
    "over_length": "Data <%s> too long, max length is %s.",
    "not_exist": "Wrong <%s>, not exist.",
    "wrong_expect": "Wrong <%s>, except a data %s.",
    "repeat": "You have added this <%s> already.",
}


def validate_type(obj, target_type, name):
    '''Validate the type of the object'''
    if not isinstance(obj, target_type):
        raise ValidationError(
            VALIDERROR_TEMPLATE["wrong_type"] % (name, target_type[0]))

def validate_exist(model, model_id, name):
    '''Validate if the object exist'''
    instance = model.query.get(model_id)
    if not instance:
        raise ValidationError(
            VALIDERROR_TEMPLATE["not_exist"] % (name,))

def validate_length(obj, max_length, name):
    '''Validate the length of the object'''
    if len(obj) > max_length:
        raise ValidationError(
            VALIDERROR_TEMPLATE["over_length"] % (name, max_length))

# Utils

def validate_timestamp(timestamp, timezone):
    # validate type
    if not isinstance(timestamp, (str, unicode)):
        raise ValidationError("Wrong <timestamp> type, expect a string type.")

    timezone = validate_timezone(timezone)
    # transfer to arrow object
    try:
        local_timestamp = arrow.get(timestamp, TIME_FORMAT).replace(tzinfo=timezone)
        utc_timestamp = local_timestamp.to('UTC')
    except Exception, e:
        raise ValidationError("Wrong <timestamp> format. E.g. '15 Dec 2015 23:12'")
    return utc_timestamp

def validate_timezone(timezone):
    if timezone:
        # validate type
        if not isinstance(timezone, (str, unicode)):
            raise ValidationError("Wrong <timezone> type, expect a string type.")
        # valid timezone exist
        if timezone not in pytz.all_timezones:
            raise ValidationError("Wrong <timezone>, not exist.")
    return timezone or DEFAULT_TIMEZONE
