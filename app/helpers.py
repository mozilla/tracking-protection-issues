#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import boto3
import botocore
from config import REGION, S3_KEY, S3_SECRET, S3_BUCKET
from flaskapp import app

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name=REGION
)


def api_post(json_payload):
    """Helper method to post junk to GitHub.


    Assumes an OAUTH_TOKEN environment variable exists."""
    repo = 'mozilla/webcompat-blipz-experiment-issues'
    headers = {
        'Authorization': 'token {0}'.format(app.config['OAUTH_TOKEN']),
        'User-Agent': 'mozilla/webcompat-blipz-experiment-issues'
    }
    uri = 'https://api.github.com/repos/{0}/issues'.format(repo)
    return requests.post(uri, data=json.dumps(json_payload), headers=headers)


def is_jpeg(filename):
    """Helper to determine if the uploaded file is a JPEG."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in set(['jpg', 'jpeg'])


def upload_file(file, bucket_name, acl='private'):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print('WTF: ', e)
        return e

    filename = "{bucket}{file}".format(
        bucket=app.config["S3_LOCATION"], file=file.filename)
    return filename
