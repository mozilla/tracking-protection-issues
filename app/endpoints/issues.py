#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from flask import abort
from flask import Blueprint
from flask import request

from app.helpers import add_comment
from app.helpers import create_issue
from app.helpers import upload_filedata

issues = Blueprint('issues', __name__)


@issues.route('/')
def index():
    """Nothing to see here."""
    return 'Hi.', 200


@issues.route('/new', methods=['POST'])
def new_issue():
    """Create a new issue.

    There is no meaningful validation here. Garbage in, garbage in.
    We expect the following sent to us as application/json:

        {"title": "string", "body": "string", "screenshot": "base64string"}

    However, if we don't get that, we return 400
    """
    DATA_URI_PREFIX = 'data:image/jpeg;base64,'

    if request.form.get('body') and request.form.get('title'):
        rv = create_issue(request.form.get('body'), request.form.get('title'))
        if rv.status_code == 201:
            if request.form.get('screenshot') and DATA_URI_PREFIX \
                    in request.form.get('screenshot'):
                issue_number = rv.json().get('number')
                # We use the newly created issue number to help name the file
                # upload in the s3 bucket.
                image_data = re.sub(DATA_URI_PREFIX, '',
                                    request.form.get('screenshot'))
                ss_uri = upload_filedata(image_data,
                                         issue_number)
                rv = add_comment(ss_uri, issue_number)
                return ('Issue created, screenshot uploaded.', rv.status_code)
            return ('Issue created (without screenshot).', 201)
        return ('Something unexpected happened, possibly.', rv.status_code)
    return abort(400)
