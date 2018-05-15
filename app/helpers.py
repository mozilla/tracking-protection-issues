#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base64 import b64decode
from io import BytesIO
import json
import re

import boto3
import requests

from config import REGION
from config import REPO
from config import S3_BUCKET
from config import S3_KEY
from config import S3_LOCATION
from config import S3_SECRET
from flaskapp import app

DATA_URI_PREFIX = 'data:image/jpeg;base64,'

HEADERS = {
    'Authorization': 'token {0}'.format(app.config['OAUTH_TOKEN']),
    'User-Agent': 'mozilla/webcompat-blipz-experiment-issues'
}

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name=REGION
)


def create_issue(body, title):
    """Helper method to create a new issue on GitHub."""
    uri = 'https://api.github.com/repos/{0}/issues'.format(REPO)
    payload = {"body": body, "title": title}
    return requests.post(uri, data=json.dumps(payload), headers=HEADERS)


def add_comment(screenshot_uri, issue_number):
    """Helper method to add a comment to an existing issue."""

    uri = 'https://api.github.com/repos/{repo}/issues/{number}/comments'.format(  # nopep8
        repo=REPO, number=issue_number
    )
    body = {"body": "Associated screenshot: {}".format(screenshot_uri)}
    return requests.post(uri, data=json.dumps(body), headers=HEADERS)


def upload_filedata(imagedata, issue_number):
    filename = "issue-{}-screenshot.jpg".format(issue_number)
    try:
        s3.upload_fileobj(
            imagedata, S3_BUCKET, filename,
            ExtraArgs={'ACL': 'private', 'ContentType': 'image/jpeg'}
        )
    except Exception as e:
        print('Error uploading image to s3: ', e)
        return e

    fileuri = "{bucket}{file}".format(bucket=S3_LOCATION, file=filename)
    return fileuri


def valid_issue_request(body, title):
    """Determine if we have required arguments.

    If body or title are missing, we return False.
    """
    if body and title:
        return True
    return False


def has_valid_screenshot(imagedata):
    """Determine if the screenshot is a base64 JPEG."""
    if imagedata and DATA_URI_PREFIX in imagedata:
        return True
    return False


def get_screenshot(imagedata):
    """Get the screenshot data.

    Return the base64 string without the prefix. Otherwise, return None.
    """
    try:
        imagedata = re.sub(DATA_URI_PREFIX, '', imagedata)
        bindata = BytesIO(b64decode(imagedata))
        return bindata
    except Exception as e:
        print('Error decoding screenshot data', e)
        return None
