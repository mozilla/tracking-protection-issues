#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Module that holds our server app code."""

from endpoints.issues import issues
from flaskapp import app

app.register_blueprint(issues, url_prefix='/')
