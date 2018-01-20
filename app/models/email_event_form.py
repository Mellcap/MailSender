#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Email, Length


class EmailEventForm(FlaskForm):
    event_id = IntegerField('Event Id', validators=[InputRequired()])
    email_group_id = IntegerField('Email Group Id', validators=[InputRequired()])
    email_subject = StringField('Email Subject', validators=[InputRequired(), Length(max=128)])
    email_content = TextAreaField('Email Content', validators=[InputRequired()])
    timestamp = StringField('Timestamp(E.g. "15 Dec 2015 23:12")', validators=[InputRequired()])
    timezone = StringField('Timezone(Default=Asia/Singapore)')
    submit = SubmitField('Submit')
