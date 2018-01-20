#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash

from app.exceptions import ValidationError
from app.form import form
from app.models.email_event import EmailEvent
from app.models.email_event_form import EmailEventForm
from app.utils import validate_timestamp


# ======
# form
# ======

@form.route('/save_emails', methods=['GET', 'POST'])
def form_save_emails():
    emailEvent_form = EmailEventForm()
    if emailEvent_form.validate_on_submit():
        # validate input timestamp
        try:
            utc_timestamp = validate_timestamp(emailEvent_form.timestamp.data, emailEvent_form.timezone.data)
        except ValidationError, e_valid:
            flash(e_valid.message, 'error')
            return redirect(url_for('api.form_save_emails'))

        # validate other data
        emailEvent = EmailEvent(
            event_id=emailEvent_form.event_id.data,
            email_group_id=emailEvent_form.email_group_id.data,
            email_subject=emailEvent_form.email_subject.data,
            email_content=emailEvent_form.email_content.data,
            timestamp=utc_timestamp
        )
        try:
            emailEvent.save()
        except ValidationError, e_valid:
            flash(e_valid.message, 'error')
        except Exception, e:
            flash(e.message, 'error')
        else:
            flash('Submit success!')
        finally:
            return redirect(url_for('form.form_save_emails'))
    return render_template('save_emails.html', form=emailEvent_form)
