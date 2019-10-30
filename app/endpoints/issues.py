#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from flask import abort
from flask import Blueprint
from flask import escape
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

    # Note: we want an empty string as a default, rather than None because
    # otherwise the string 'None' wouldn't fail valid_issue_request
    body = escape(request.form.get('body', ''))
    labels = escape(request.form.get('labels', ''))
    title = escape(request.form.get('title', ''))

    if not valid_issue_request(body, title):
        return abort(400)

    # No labels means we're not doing any blocking, so let's not report.
    # The client should not offer a possibility to send these reports,
    # but lets prevent processing them here as a stop-gap.
    if not labels:
        # The client currently can't fully handle missing labels or
        # error responses from the server, so let's grudgingly return a
        # 200 here, see https://bugzilla.mozilla.org/show_bug.cgi?id=1582751
        return ('Missing labels', 200)

    labels = [label.strip() for label in labels.split(',')]

    rv = create_issue(body, title, labels)
    if rv.status_code == 201:
        return ('Issue created.', 201)
    return ('Something unexpected happened, possibly.', rv.status_code)
