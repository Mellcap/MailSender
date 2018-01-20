#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class EmailGroupForm(FlaskForm):
    group_name = StringField('Email Group Name', validators=[InputRequired(), Length(max=64)])
    email_addresses = TextAreaField(
        'Email Addresses(You can input multi emails, divided them by comma.)', validators=[InputRequired()])
    submit = SubmitField('Submit')
