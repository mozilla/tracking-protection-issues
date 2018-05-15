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
COMMENT_ENDPOINT = 'https://api.github.com/repos/test/test-repo/issues/1/comments'  # noqa
S3_ENDPOINT = 'https://test-bucket.s3.test-region.amazonaws.com'


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
        rv = self.app.post('/new', data=json.dumps(dict(hi='dude')))
        self.assertEqual(rv.status_code, 400)

    @responses.activate
    def test_create_issue(self):
        """Test new issue endpoint without screenshot."""
        responses.add(responses.POST,
                      ISSUE_ENDPOINT,
                      json='{"number": "1"}',
                      status=201,
                      content_type='application/json')

        rv = self.app.post(
            '/new', data=dict(title='hi', body='dude')
        )
        self.assertEqual(rv.status_code, 201)

    @responses.activate
    def test_create_issue_good_screenshot(self):
        """Test new issue endpoint with a good screenshot."""
        responses.add(responses.POST,
                      ISSUE_ENDPOINT,
                      body='{"number": "1"}',
                      status=201,
                      content_type='application/json')
        responses.add(responses.PUT,
                      S3_ENDPOINT,
                      json='{}',
                      status=200)
        responses.add(responses.POST,
                      COMMENT_ENDPOINT,  # nopep8
                      json='{}',
                      status=201)

        fake_jpg = 'sup'
        # add padding to avoid TypeError: Incorrect padding
        fake_jpg += "=" * ((4 - len(fake_jpg) % 4) % 4)
        rv = self.app.post(
            '/new',
            data=dict(title='hi',
                      body='dude',
                      screenshot='data:image/jpeg;base64,{}'.format(fake_jpg))
        )
        self.assertEqual(rv.status_code, 201)
        self.assertIn('screenshot uploaded', rv.data)

    @responses.activate
    def test_create_issue_bad_screenshot(self):
        """Test new issue endpoint with a bad screenshot."""
        responses.add(responses.POST,
                      ISSUE_ENDPOINT,
                      body='{"number": "1"}',
                      status=201,
                      content_type='application/json')
        responses.add(responses.PUT,
                      S3_ENDPOINT,
                      json='{}',
                      status=200)
        responses.add(responses.POST,
                      COMMENT_ENDPOINT,  # nopep8
                      json='{}',
                      status=201)

        rv = self.app.post(
            '/new', data=dict(title='hi', body='dude',
                              screenshot='data:image/png;base64,sup')
        )
        self.assertEqual(rv.status_code, 201)
        self.assertIn('without screenshot', rv.data)
