#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length


class EmailEventForm(FlaskForm):
    event_id = IntegerField('Event Id', validators=[InputRequired()])
    email_group_id = SelectField('Email Group Id', coerce=int, validators=[InputRequired()])
    email_subject = StringField('Email Subject', validators=[InputRequired(), Length(max=128)])
    email_content = TextAreaField('Email Content', validators=[InputRequired()])
    timestamp = StringField('Timestamp', validators=[InputRequired()])
    timezone = StringField('Timezone')
    submit = SubmitField('Submit')
