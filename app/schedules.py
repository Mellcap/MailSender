#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import arrow

from app import celery, create_app
from app.models.email_event import EmailEvent
from app.email import send_email


@celery.task
def schedule_send_emails():
    now = arrow.utcnow().replace(second=0, microsecond=0)
    app = create_app(os.getenv('JUBLIA_CONFIG') or 'default')
    with app.app_context():
        # find email_events need to be send.
        target_emailEvents = find_target_emailEvents(timestamp=now)
        for email_event in target_emailEvents:
            # send email
            send_email.delay(email_event.id)


def find_target_emailEvents(timestamp):
    '''
    Find email_events need to be send.
    **timestamp==now & is_send=False
    '''
    target_emailEvents = EmailEvent.query.filter_by(timestamp=timestamp, is_send=False).all()
    return target_emailEvents

