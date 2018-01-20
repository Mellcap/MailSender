#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from app import db
# from app.exceptions import ValidationError
# from app.utils import VALIDERROR_TEMPLATE, validate_type, validate_length


email_group2address = db.Table('email_group2addresses',
    db.Column('email_group_id', db.Integer, db.ForeignKey('email_groups.id'), primary_key=True),
    db.Column('email_address_id', db.Integer, db.ForeignKey('email_addresses.id'), primary_key=True)
)


class EmailGroup(db.Model):
    __tablename__ = 'email_groups'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64), unique=True)
    email_addresses = db.relationship('EmailAddress', secondary=email_group2address, lazy='subquery',
        backref=db.backref('email_groups', lazy=True))

    def __repr__(self):
        return '<EmailGroup: %s: %s>' % (self.id, self.group_name)


class EmailAddress(db.Model):
    __tablename__ = 'email_addresses'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<EmailAddress: %s: %s>' % (self.id, self.email_address)
