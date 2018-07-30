#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for our basic app endpoints."""

import json
import os
import sys
import unittest

import responses

# Add issue module to import path
sys.path.append(os.path.realpath(os.pardir))
from app import app  # noqa

ISSUE_ENDPOINT = 'https://api.github.com/repos/test/test-repo/issues'


class TestEndpoints(unittest.TestCase):
    """Module for testing the form."""

    def setUp(self):
        """Set up."""
        app.config['TESTING'] = True
        self.app = app.test_client()

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

    @responses.activate
    def test_create_issue(self):
        """Test new issue endpoint."""
        responses.add(responses.POST,
                      ISSUE_ENDPOINT,
                      json='{"number": "1"}',
                      status=201,
                      content_type='application/json')

        rv = self.app.post(
            '/new', data=dict(title='hi', body='dude')
        )
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post(
            '/new', data=dict(title='hi', body='dude', labels=['wow'])
        )
        self.assertEqual(rv.status_code, 201)
