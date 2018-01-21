#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash
from app.exceptions import ValidationError
from app.form import form
from app.models.email_group import EmailGroup
from app.models.email_group_form import EmailGroupForm


# ======
# form
# ======

@form.route('/save_email_groups', methods=['GET', 'POST'])
def form_email_groups():
    emailGroup_form = EmailGroupForm()
    if emailGroup_form.validate_on_submit():
        # validate input data
        emailGroup = EmailGroup(group_name=emailGroup_form.group_name.data)
        try:
            emailGroup.validate()
            # add batch email_address
            emailGroup.add_batch_emailAddresses_from_string(emailGroup_form.email_addresses.data)
            emailGroup.save()
        except ValidationError, e_valid:
            flash(e_valid.message, 'alert-danger')
        except Exception, e:
            flash(e.message, 'alert-danger')
        else:
            flash('Submit success!', 'alert-success')
        finally:
            return redirect(url_for('form.form_email_groups'))
    return render_template('save_email_groups.html', form=emailGroup_form)
