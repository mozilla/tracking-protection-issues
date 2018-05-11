#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

# The following environment variables are assumed to exist:
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', 'test')
PRODUCTION = os.environ.get('PRODUCTION', 0)
REGION = os.environ.get('REGION', 'test')
REPO = os.environ.get('REPO', 'test/test')
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", 'test')
S3_KEY = os.environ.get("S3_ACCESS_KEY", 'test')
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY", 'test')

S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
SECRET_KEY = os.urandom(32)

DEBUG = False
if not PRODUCTION:
    DEBUG = True
