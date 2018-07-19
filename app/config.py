#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

# The following environment variables are assumed to exist:
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', 'test-token')
PRODUCTION = os.environ.get('PRODUCTION', 0)
REPO = os.environ.get('REPO', 'test/test-repo')
SECRET_KEY = os.urandom(32)

DEBUG = False
if not PRODUCTION:
    DEBUG = True
