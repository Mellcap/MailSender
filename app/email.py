#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask_mail import Message

from app.models.email_event import EmailEvent
from app.models.email_group import  EmailGroup
from app import mail, celery, create_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def send_email(email_event_id):
    app = create_app(os.getenv('JUBLIA_CONFIG') or 'default')
    with app.app_context():
        # find email_event
        email_event = EmailEvent.query.get(email_event_id)
        # check the email_event exist & not send
        if not email_event or email_event.is_send:
            return
        # get recipients in this email_group
        recipients = get_recipients(app, email_event.email_group_id)
        if not recipients:
            return
        # send email
        msg = Message(subject=email_event.email_subject,
                      recipients=recipients,
                      body=email_event.email_content)
        try:
            mail.send(msg)
            # change is_send=True
            email_event.success_send()
        except Exception, e:
            # if failed, log the error.
            logger.error('Send email failed, <email_event_id:%s>, message: %s' % (email_event_id, e))

def get_recipients(app, email_group_id):
    '''Get recipients in this email_group'''
    with app.app_context():
        email_group = EmailGroup.query.get(email_group_id)
        # check the email_group exist
        if not email_group:
            return
        # return the email_address list(recipients)
        return [a.email_address for a in email_group.email_addresses]
