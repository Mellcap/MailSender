#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify

from app.api import api
from app.models.email_event import EmailEvent
from app.utils import SUCCESS_MESSAGE, validate_timestamp


# ----
# api
# ----

@api.route('/save_emails', methods=['POST'])
def save_emails():
    """
    Save email data to db.
    ---
    Method: POST
    @param: event_id int
    @param: email_group_id int
    @param: email_subject str
    @param: email_content str
    @param: timestamp str
    @param: timezone str notRequired default=Asia/Singapore
    """
    request_data = request.json
    utc_timestamp = validate_timestamp(request_data['timestamp'], request_data.get('timezone'))
    if utc_timestamp:
        email_event = EmailEvent(
            event_id=request_data['event_id'],
            email_group_id=request_data['email_group_id'],
            email_subject=request_data['email_subject'],
            email_content=request_data['email_content'],
            timestamp=utc_timestamp
        )
        email_event.save()

        return jsonify(SUCCESS_MESSAGE)
