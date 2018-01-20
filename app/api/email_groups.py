#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify

from app.api import api
from app.models.email_group import EmailGroup, EmailAddress
from app.utils import SUCCESS_MESSAGE, SUCCESS_CREATE_MESSAGE, NOT_FOUND_MESSAGE


# ----
# api
# ----

@api.route('/email_groups', methods=['POST'])
def create_email_group():
    """
    Create new email_group
    ---
    Method: POST
    @param: group_name str unique
    """
    request_data = request.json

    # create new email_group
    email_group = EmailGroup(group_name=request_data['group_name'])
    email_group.save()

    # return success message
    ret_msg = {'email_group_id': email_group.id}
    ret_msg.update(SUCCESS_CREATE_MESSAGE)
    return jsonify(ret_msg)


@api.route('/email_groups/<int:email_group_id>/email_addresses', methods=['POST'])
def create_email_addresses_in_group(email_group_id):
    """
    Create new /email_addresses in a certain email_group
    ---
    Method: POST
    @param: email_group_id int
    @param: email_addresses str // if many, divided by comma
    """
    request_data = request.json

    # get email_group
    email_group = EmailGroup.query.get(email_group_id)
    # if email_group not exist, return 404
    if not email_group:
        return jsonify(NOT_FOUND_MESSAGE)
    # add batch email_address
    email_group.add_batch_emailAddresses_from_string(request_data['email_addresses'])

    # return success message
    ret_msg = {'email_group_id': email_group.id}
    ret_msg.update(SUCCESS_CREATE_MESSAGE)
    return jsonify(ret_msg)


@api.route('/email_addresses', methods=['POST'])
def create_email_address():
    """
    Create new email_address
    ---
    Method: POST
    @param: group_name str unique
    """
    request_data = request.json
    email_address = EmailAddress(email_address=request_data['email_address'])
    email_address.save()

    return jsonify(SUCCESS_MESSAGE)
