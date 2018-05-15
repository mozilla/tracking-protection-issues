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
from app.helpers import get_screenshot
from app.helpers import has_valid_screenshot
from app.helpers import upload_filedata
from app.helpers import valid_issue_request

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

    body = request.form.get('body')
    title = request.form.get('title')
    screenshot = request.form.get('screenshot')

    if valid_issue_request(body, title):
        rv = create_issue(body, title)
        if rv.status_code == 201:
            if has_valid_screenshot(screenshot):
                issue_number = rv.json().get('number')
                # We use the newly created issue number to help name the file
                # upload in the s3 bucket.
                image_data = get_screenshot(screenshot)
                ss_uri = upload_filedata(image_data, issue_number)
                rv = add_comment(ss_uri, issue_number)
                return ('Issue created, screenshot uploaded.', rv.status_code)
            return ('Issue created (without screenshot).', 201)
        return ('Something unexpected happened, possibly.', rv.status_code)
    return abort(400)
