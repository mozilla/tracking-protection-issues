#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re

import requests

from config import REPO
from flaskapp import app

HEADERS = {
    'Authorization': 'token {0}'.format(app.config['OAUTH_TOKEN']),
    'User-Agent': 'mozilla/webcompat-blipz-experiment-server'
}


def find_issue(title):
    """Helper method to find issues on GitHub."""
    # We filter out older issues to avoid huge result sets and sort by created
    # date to avoid commenting on two different issues.
    uri = "https://api.github.com/search/issues?q='{0}'+in:title+type:issue+repo:{1}+created:>=2019-10-19&sort=created&order=desc".format(title, REPO)  # noqa
    return requests.get(uri, headers=HEADERS)


def add_labels(issue_id, labels):
    """Helper method to add labels to an existing issue on GitHub."""
    uri = 'https://api.github.com/repos/{0}/issues/{1}/labels'.format(REPO,
                                                                      issue_id)
    payload = {"labels": labels}
    return requests.post(uri, data=json.dumps(payload), headers=HEADERS)


def create_issue(body, title, labels):
    """Helper method to create a new issue on GitHub."""
    # We try to find an existing issue with the same title (domain),
    # and add a comment and the additional tags if it exists.
    rv = find_issue(title)
    if rv.status_code == 200:
        data = rv.json()
        if data['total_count'] >= 1:
            issue = data['items'][0]
            issue_id = issue['number']
            add_labels(issue_id, labels)
            uri = 'https://api.github.com/repos/{0}/issues/{1}/comments'.format(REPO, issue_id)  # noqa
            payload = {"body": body}
            return requests.post(uri, data=json.dumps(payload),
                                 headers=HEADERS)
    uri = 'https://api.github.com/repos/{0}/issues'.format(REPO)
    payload = {"body": body, "title": title, "labels": labels}
    return requests.post(uri, data=json.dumps(payload), headers=HEADERS)


def valid_issue_request(body, title):
    """Determine if we have required arguments.

    If body or title are missing, we return False.
    """
    if body and title:
        return True
    return False
