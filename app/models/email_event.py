#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
from sqlalchemy_utils import ArrowType

from app import db
from app.models.email_group import EmailGroup
# from app.exceptions import ValidationError
# from app.utils import VALIDERROR_TEMPLATE, validate_type, validate_length, validate_exist


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
