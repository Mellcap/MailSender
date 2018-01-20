#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from app import db
from app.exceptions import ValidationError
from app.utils import VALIDERROR_TEMPLATE, validate_type, validate_length


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

    def validate(self):
        '''validate the input fileds'''
        self.validate_groupName()

    def validate_groupName(self):
        '''Valudate: type & length & repeat'''
        # validate type
        validate_type(obj=self.group_name, target_type=(str, unicode), name='group_name')
        # validate length
        validate_length(obj=self.group_name, max_length=64, name='group_name')
        # validate repeat group_name
        repeat_groupName = self.query.filter_by(group_name=self.group_name).first()
        if repeat_groupName and repeat_groupName.id != self.id:
            raise ValidationError(VALIDERROR_TEMPLATE["repeat"] % ('email_group',))

    def add_email_address(self, email_address):
        '''Add email_address into this group'''
        self.email_addresses.append(email_address)
        self.commit()

    def add_batch_emailAddresses_from_obj(self, email_addresses):
        '''
        Add batch email_address into this group.
        **email_addresses is a list of EmailAddress object.
        '''
        for email_address in email_addresses:
            self.email_addresses.append(email_address)
        self.commit()

    def add_batch_emailAddresses_from_string(self, email_addresses):
        '''
        Add batch email_address into this group.
        **email_addresses is a string devided by comma.
        '''
        for email_address in email_addresses.split(','):
            if email_address:
                email_address_obj = EmailAddress.get_or_create_emailAddress(email_address=email_address.strip())
                self.email_addresses.append(email_address_obj)
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


class EmailAddress(db.Model):
    __tablename__ = 'email_addresses'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<EmailAddress: %s: %s>' % (self.id, self.email_address)

    def validate(self):
        '''validate the input fileds'''
        self.validate_emailAddress()

    def validate_emailAddress(self):
        '''Valudate: type & length & format & repeat'''
        # validate type
        validate_type(obj=self.email_address, target_type=(str, unicode), name='email_address')
        # validate length
        validate_length(obj=self.email_address, max_length=64, name='email_address')
        # validate email format
        self.validate_emailFormat(email_address=self.email_address)
        # validate repeat group_name
        repeat_emailAddress = self.query.filter_by(email_address=self.email_address).first()
        if repeat_emailAddress and repeat_emailAddress.id != self.id:
            raise ValidationError(VALIDERROR_TEMPLATE["repeat"] % ('email_address',))

    def validate_emailFormat(self, email_address):
        '''Valudate: email format'''
        regex_email = r'\b[\w.-]+?@\w+?\.\w+?\b'
        if not re.findall(regex_email, email_address):
            raise ValidationError(
                VALIDERROR_TEMPLATE["wrong_expect"] % ('email_address', 'E.g. imellcap@gmail.com'))

    @classmethod
    def get_or_create_emailAddress(cls, email_address):
        '''Get or create the email_address in database.'''
        # try to get email_address_obj
        email_address_obj = cls.query.filter_by(email_address=email_address).first()
        if not email_address_obj:
            # create and validate email_address_obj
            email_address_obj = cls(email_address=email_address)
            email_address_obj.validate()
        return email_address_obj

    # Basic Method
    def save(self):
        '''Save data into database'''
        self.validate()
        self.commit()

    def commit(self):
        '''Commit change'''
        db.session.add(self)
        db.session.commit()