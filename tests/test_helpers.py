#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for helper methods."""

from io import BufferedIOBase
import json
import os
import sys
import unittest

import responses

# Add issue module to import path
sys.path.append(os.path.realpath(os.pardir))
from app import app  # noqa
from app.helpers import valid_issue_request  # noqa


class TesHelpers(unittest.TestCase):
    """Module for testing the helpers module."""

    def setUp(self):
        """Set up."""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """Tear down."""
        pass

    def test_valid_issue_request(self):
        # Note, we're just testing truthiness, and not exhaustively.
        self.assertTrue(valid_issue_request("cool", "hi"))
        self.assertFalse(valid_issue_request("cool", ""))
        self.assertFalse(valid_issue_request("", "hi"))
        self.assertFalse(valid_issue_request("", ""))
