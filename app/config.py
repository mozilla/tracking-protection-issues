#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

# These are all set as heroku environement variables
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', '')
PRODUCTION = os.environ.get('PRODUCTION', 0)
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", '')
S3_KEY = os.environ.get("S3_ACCESS_KEY", '')
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY", '')
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
SECRET_KEY = os.urandom(32)

DEBUG = False
if not PRODUCTION:
    DEBUG = True
