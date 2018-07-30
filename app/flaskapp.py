#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
import logging

app = Flask(__name__)
app.config.from_pyfile("config.py")

# disable logs so we don't record IP addresses
# note: we may have to turn this on in the future if we detect abuse.
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True
