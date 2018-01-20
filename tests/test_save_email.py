#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app import create_app, db
from app.models.email_event import EmailEvent
from app.models.email_group import EmailGroup, EmailAddress
from tests.utils import generate_timestamp
from app.utils import VALIDERROR_TEMPLATE
from app.exceptions import ValidationError

# Constant
TEMP_EMAIL_ADDRESS = "imellcap@gmail.com"
TEMP_EMAIL_SUBJECT = "Hello, Mellcap!"
TEMP_EMAIL_CONTENT = "This is a test email."
TEMP_GROUP_NAME = "default_email_group"


class SaveEmailTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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

    def inital_emailAddress(self, email_address=TEMP_EMAIL_ADDRESS):
        valid_emailAddress = EmailAddress(email_address=email_address)
        valid_emailAddress.save()
        return valid_emailAddress

    # =====================================
    #  EMAIL Event
    # =====================================

    # ===============
    # event id
    # ===============

    def test_eventId_valid(self):
        mailEvent = self.initial_emailEvent()
        valid_eventId = 8
        mailEvent.event_id = valid_eventId
        mailEvent.save()
        self.assertEqual(mailEvent.event_id, valid_eventId)

    def test_eventId_type(self):
        mailEvent = self.initial_emailEvent()
        wrongType_eventId = '123'
        mailEvent.event_id = wrongType_eventId
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('event_id', int)):
            mailEvent.save()

    # ===============
    # email group id
    # ===============

    def test_emailGroupId_type(self):
        mailEvent = self.initial_emailEvent()
        wrongType_emailGroupId = '123'
        mailEvent.email_group_id = wrongType_emailGroupId
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('email_group_id', int)):
            mailEvent.save()

    # ===============
    # email address
    # ===============

    def test_emailSubject_valid(self):
        mailEvent = self.initial_emailEvent()
        # test Unicode
        valid_emailSubject = u'你好'
        mailEvent.email_subject = valid_emailSubject
        mailEvent.save()
        self.assertEqual(mailEvent.email_subject, valid_emailSubject)

    def test_emailSubject_type(self):
        mailEvent = self.initial_emailEvent()
        wrongType_emailSubject = 123
        mailEvent.email_subject = wrongType_emailSubject
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('email_subject', str)):
            mailEvent.save()

    # ===============
    # email content
    # ===============

    def test_emailContent_valid(self):
        mailEvent = self.initial_emailEvent()
        # test Unicode
        valid_emailContent = u'你好'
        mailEvent.email_content = valid_emailContent
        mailEvent.save()
        self.assertEqual(mailEvent.email_content, valid_emailContent)

    def test_emailContent_type(self):
        mailEvent = self.initial_emailEvent()
        wrongType_emailContent = 123
        mailEvent.email_content = wrongType_emailContent
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('email_content', str)):
            mailEvent.validate()

    # =================
    # email timestamp
    # =================

    def test_timestamp_valid(self):
        mailEvent = self.initial_emailEvent()
        valid_emailTimestamp = generate_timestamp()
        mailEvent.timestamp = valid_emailTimestamp
        mailEvent.save()
        self.assertEqual(mailEvent.timestamp, valid_emailTimestamp)

    def test_timestamp_afterNow(self):
        mailEvent = self.initial_emailEvent()
        invalid_emailTimestamp = generate_timestamp(valid=False)
        mailEvent.timestamp = invalid_emailTimestamp
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_expect"] % ('timestamp', 'after now')):
            mailEvent.save()

    # ===============
    # email repeat
    # ===============

    def test_emailEvent_repeat(self):
        mail_event1 = self.initial_emailEvent()
        mail_event2 = self.initial_emailEvent(shift_hours=2, email_group_id=mail_event1.email_group_id)
        # make mail_event2 == mail_event1
        mail_event2.timestamp = mail_event1.timestamp
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["repeat"] % ('email_event',)):
            mail_event2.save()


    # =====================================
    #  EMAIL GROUP
    # =====================================

    # ===============
    # group name
    # ===============

    def test_groupName_valid(self):
        mailGroup = self.initial_emailGroup()
        # test Unicode
        valid_groupName = u'你好'
        mailGroup.group_name = valid_groupName
        mailGroup.save()
        self.assertEqual(mailGroup.group_name, valid_groupName)

    def test_groupName_type(self):
        mailGroup = self.initial_emailGroup()
        wrongType_groupName = 123
        mailGroup.group_name = wrongType_groupName
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('group_name', str)):
            mailGroup.save()

    def test_groupName_length(self):
        mailGroup = self.initial_emailGroup()
        wrongLength_groupName = 'a' * 65
        mailGroup.group_name = wrongLength_groupName
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["over_length"] % ('group_name', 64)):
            mailGroup.save()

    def test_groupName_repeat(self):
        mailGroup1 = self.initial_emailGroup()
        # make mailGroup2.group_name == mailGroup1.group_name
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["repeat"] % ('email_group',)):
            mailGroup2 = self.initial_emailGroup()

    # =====================================
    #  EMAIL ADDRESS
    # =====================================

    # ===============
    # email address
    # ===============

    def test_emailAddress_valid(self):
        emailAddress = self.inital_emailAddress()
        valid_emailAddress = 'mellcap@mail.com'
        emailAddress.email_address = valid_emailAddress
        emailAddress.save()
        self.assertEqual(emailAddress.email_address, valid_emailAddress)

    def test_emailAddress_type(self):
        emailAddress = self.inital_emailAddress()
        wrongType_emailAddress = 123
        emailAddress.email_address = wrongType_emailAddress
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_type"] % ('email_address', str)):
            emailAddress.save()

    def test_emailAddress_length(self):
        emailAddress = self.inital_emailAddress()
        wrongLength_emailAddress = 'a' * 65
        emailAddress.email_address = wrongLength_emailAddress
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["over_length"] % ('email_address', 64)):
            emailAddress.save()

    def test_emailAddress_format(self):
        emailAddress = self.inital_emailAddress()
        wrongFormat_mailAddress = 'abc@bcd'
        emailAddress.email_address = wrongFormat_mailAddress
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["wrong_expect"] % (
                                     'email_address', 'E.g. imellcap@gmail.com')):
            emailAddress.save()

    def test_emailAddress_repeat(self):
        emailAddress1 = self.inital_emailAddress()
        # make emailAddress2.address == emailAddress1.address
        with self.assertRaisesRegexp(ValidationError,
                                     VALIDERROR_TEMPLATE["repeat"] % ('email_address',)):
            emailAddress2 = self.inital_emailAddress()
