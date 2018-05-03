#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os

import requests

from flask import abort
from flask import Flask
from flask import request

app = Flask(__name__)


def api_post(json_payload):
    """Helper method to post junk to GitHub.


    Assumes an OAUTH_TOKEN environment variable exists."""
    repo = 'mozilla/webcompat-blipz-experiment-issues'
    headers = {
        'Authorization': 'token {0}'.format(os.environ['OAUTH_TOKEN']),
        'User-Agent': 'mozilla/webcompat-blipz-experiment-issues'
    }
    uri = 'https://api.github.com/repos/{0}/issues'.format(repo)
    return requests.post(uri, data=json.dumps(json_payload), headers=headers)


@app.route('/')
def index():
    """Nothing to see here."""
    return 'Hi.', 200


@app.route('/new', methods=['POST'])
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
