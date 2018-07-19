#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base64 import b64decode
from io import BytesIO
import json
import re

import requests

from config import REPO
from flaskapp import app

HEADERS = {
    'Authorization': 'token {0}'.format(app.config['OAUTH_TOKEN']),
    'User-Agent': 'mozilla/webcompat-blipz-experiment-server'
}


def create_issue(body, title, labels=None):
    """Helper method to create a new issue on GitHub."""
    uri = 'https://api.github.com/repos/{0}/issues'.format(REPO)
    payload = {"body": body, "title": title}
    if labels:
        payload['labels'] = labels.split(', ')
    return requests.post(uri, data=json.dumps(payload), headers=HEADERS)


def valid_issue_request(body, title):
    """Determine if we have required arguments.

    If body or title are missing, we return False.
    """
    if body and title:
        return True
    return False
