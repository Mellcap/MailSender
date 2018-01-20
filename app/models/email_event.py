#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
from sqlalchemy_utils import ArrowType

from app import db
from app.models.email_group import EmailGroup
from app.exceptions import ValidationError
from app.utils import VALIDERROR_TEMPLATE, validate_type, validate_length, validate_exist


class EmailEvent(db.Model):
    __tablename__ = 'email_events'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_group_id = db.Column(db.Integer, db.ForeignKey('email_groups.id'))
    email_subject = db.Column(db.String(128))
    email_content = db.Column(db.Text)
    timestamp = db.Column(ArrowType, index=True)
    is_send = db.Column(db.Boolean, default=False, index=True)

    def __repr__(self):
        return '<EmailEvent: %s, timestamp: %s>' % (self.id, self.timestamp)

    def validate(self):
        '''validate the input fileds'''
        self.valid_evenId()
        self.validate_emailGroupId()
        self.validate_emailContent()
        self.validate_emailSubject()
        self.validate_timestamp()

        # validate repeat
        self.validate_repeat()

    def valid_evenId(self):
        '''Valudate: type'''
        validate_type(obj=self.event_id, target_type=(int, long), name='event_id')

    def validate_emailGroupId(self):
        '''Valudate: type & exist'''
        # validate type
        validate_type(obj=self.email_group_id, target_type=(int, long), name='email_group_id')
        # validate exist
        validate_exist(EmailGroup, self.email_group_id, 'email_group_id')

    def validate_emailSubject(self):
        '''Valudate: type & length'''
        # validate type
        validate_type(obj=self.email_subject, target_type=(str, unicode), name='email_subject')
        # validate length
        validate_length(obj=self.email_subject, max_length=128, name='email_subject')

    def validate_emailContent(self):
        '''Valudate: type'''
        validate_type(obj=self.email_content, target_type=(str, unicode), name='email_content')

    def validate_timestamp(self):
        '''Valudate: time, make sure timestamp > now'''
        now = arrow.utcnow()
        if self.timestamp <= now:
            raise ValidationError(
                VALIDERROR_TEMPLATE["wrong_expect"] % ('timestamp', 'after now'))

    def validate_repeat(self):
        '''Valudate: repeat'''
        repeat_emailEvent = self.query.filter_by(
            event_id=self.event_id,
            email_group_id=self.email_group_id,
            email_subject = self.email_subject,
            email_content=self.email_content,
            timestamp=self.timestamp
        ).first()
        if repeat_emailEvent and repeat_emailEvent.id != self.id:
            raise ValidationError(VALIDERROR_TEMPLATE["repeat"] % ('email_event',))

    def success_send(self):
        '''Send mail success, set is_send=True'''
        self.is_send = True
        self.commit()

    # Basic Method
    def save(self):
        '''Save data into database'''
        self.validate()
        self.commit()

    def commit(self):
        '''Commit change'''
        db.session.add(self)
        db.session.commit()
