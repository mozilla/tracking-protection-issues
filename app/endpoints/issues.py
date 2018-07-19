#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from flask import abort
from flask import Blueprint
from flask import request

from app.helpers import create_issue
from app.helpers import valid_issue_request

issues = Blueprint('issues', __name__)


@issues.route('/')
def index():
    """Nothing to see here."""
    return '200 OK', 200


@issues.route('/new', methods=['POST'])
def new_issue():
    """Create a new issue.

    There is no meaningful validation here. Garbage in, garbage in.
    We expect the following sent to us as application/json:

        {"title": "string", "body": "string",
         "labels": "comma, separated, string"}

    However, if we don't get that, we return 400
    """

    body = request.form.get('body')
    labels = request.form.get('labels')
    title = request.form.get('title')

    if valid_issue_request(body, title):
        rv = create_issue(body, title, labels)
        if rv.status_code == 201:
            return ('Issue created.', 201)
        return ('Something unexpected happened, possibly.', rv.status_code)
    return abort(400)
