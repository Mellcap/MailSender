#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random
from app import create_app, db, celery, mail
from app.schedules import find_target_emailEvents
from app.models.email_event import EmailEvent
from app.models.email_group import EmailGroup, EmailAddress
from tests.utils import generate_timestamp

# Constant
TEMP_EMAIL_ADDRESS = "imellcap@gmail.com"
TEMP_EMAIL_SUBJECT = "Hello, Mellcap!"
TEMP_EMAIL_CONTENT = "This is a test email."
TEMP_GROUP_NAME = "default_email_group"


class SendEmailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # make sure in testing environment, it will not send the email
        self.assertTrue(self.app.testing)
        db.create_all()
        # make celery sync
        celery.conf.update(CELERY_ALWAYS_EAGER=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def initial_emailEvent(self, event_id=1, shift_hours=1, email_group_id=None):
        if not email_group_id:
            email_group_id = self.initial_emailGroup().id
        valid_mailEvent = EmailEvent(
            event_id=event_id,
            email_group_id=email_group_id,
            email_subject=TEMP_EMAIL_SUBJECT,
            email_content=TEMP_EMAIL_CONTENT,
            timestamp=generate_timestamp(shift_hours=shift_hours)
        )
        valid_mailEvent.save()
        return valid_mailEvent

    def initial_emailGroup(self, group_name=TEMP_GROUP_NAME):
        valid_emailGroup = EmailGroup(group_name=group_name)
        valid_emailGroup.save()
        return valid_emailGroup

    def get_address_from_emailEvent(self, email_event):
        email_group_id = email_event.email_group_id
        email_group = EmailGroup.query.get(email_group_id)
        return [i.email_address for i in email_group.email_addresses]

    def inital_emailAddress(self, email_address=TEMP_EMAIL_ADDRESS):
        valid_emailAddress = EmailAddress(email_address=email_address)
        valid_emailAddress.save()
        return valid_emailAddress

    def add_emailAddress(self, email_group_id, nums=1, email_address=TEMP_EMAIL_ADDRESS):
        email_group_obj = EmailGroup.query.get(email_group_id)
        for i in xrange(nums):
            target_email_address = email_address + 'c' * i
            email_address_obj = EmailAddress(email_address=target_email_address)
            email_group_obj.email_addresses.append(email_address_obj)

    # ===========
    # send mail
    # ===========

    def test_sendMail(self):
        with mail.record_messages() as outbox:
            mail_event = self.initial_emailEvent()
            # add email_addresses
            nums = random.randint(1, 10)
            self.add_emailAddress(email_group_id=mail_event.email_group_id, nums=nums)
            email_subject = mail_event.email_subject
            email_content = mail_event.email_content

            recipients = self.get_address_from_emailEvent(mail_event)

            mail.send_message(subject=email_subject,
                              recipients=recipients,
                              body=email_content,
                              sender="from@example.com")

            self.assertEqual(len(outbox[0].recipients), len(recipients))
            self.assertEqual(outbox[0].subject, email_subject)
            self.assertEqual(outbox[0].body, email_content)

    # ==========================
    # find target email events
    # ==========================

    def test_find_target_Events(self):
        mail_event1 = self.initial_emailEvent()
        timestamp1 = mail_event1.timestamp
        target_emailEvents1 = find_target_emailEvents(timestamp1)
        self.assertEqual(len(target_emailEvents1), 1)

        # make event1 and event2 have the same timestamp
        mail_event2 = self.initial_emailEvent(event_id=10, email_group_id=mail_event1.email_group_id)
        mail_event2.timestamp = mail_event1.timestamp
        mail_event2.save()
        target_emailEvents2 = find_target_emailEvents(timestamp1)
        self.assertEqual(len(target_emailEvents2), 2)

        # send mail_event1
        mail_event1.success_send()
        target_emailEvents3 = find_target_emailEvents(timestamp1)
        self.assertEqual(len(target_emailEvents3), 1)

    def test_notFindTargets(self):
        mail_event = self.initial_emailEvent()
        timestamp = mail_event.timestamp.shift(hours=1)
        target_emailEvents = find_target_emailEvents(timestamp)
        self.assertEqual(len(target_emailEvents), 0)



