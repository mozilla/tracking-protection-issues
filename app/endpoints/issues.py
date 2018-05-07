#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import requests

from app.flaskapp import app
from app.helpers import api_post
from app.helpers import is_jpeg
from app.helpers import upload_file
from flask import abort
from flask import Blueprint
from flask import Flask
from flask import request


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

        {"title": "string", "body": "string"}

    However, if we don't get that, we return 400
    """
    if request.json:
        rv = api_post(request.json)
        return (rv.content, rv.status_code)
    return abort(400)
