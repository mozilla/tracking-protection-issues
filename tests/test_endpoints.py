#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for our basic app endpoints."""

import json
from mock import MagicMock
from mock import patch
import os
from requests import Response
import sys
import unittest

# Add issue module to import path
sys.path.append(os.path.realpath(os.pardir))
import issue  # nopep8


class TestEndpoints(unittest.TestCase):
    """Module for testing the form."""

    def setUp(self):
        """Set up."""
        issue.app.config['TESTING'] = True
        os.environ['OAUTH_TOKEN'] = 'wowowoowowoww'
        self.app = issue.app.test_client()

    def tearDown(self):
        """Tear down."""
        pass

    def test_home(self):
        """Test that the index route exists."""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_new_issue_get(self):
        """Test that the new issue route rejects a GET."""
        rv = self.app.get('/new')
        self.assertEqual(rv.status_code, 405)

    def test_new_issue_bad_post(self):
        """Test that the new issue route rejects a POST that is malformed."""
        rv = self.app.post('/new')
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/new', data=json.dumps(dict(hi='dude')))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post(
            '/new', data=json.dumps(dict(hi='dude')),
            content_type='turkey/sandwiches'
        )
        self.assertEqual(rv.status_code, 400)

    @patch('issue.api_post')
    def test_mock_api_post(self, mock_post):
        """Test that the new issue route accepts a POST with expected data."""
        mock_post.return_value = MagicMock(
            content=json.dumps(dict(great='success')),
            status_code=201,
            spec=Response
        )

        rv = self.app.post(
            '/new', data=json.dumps(dict(hi='dude')),
            content_type='application/json'
        )
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.get_json(force=True).get('great'), 'success')
