import json
import unittest
from unittest.mock import patch

from zume import app
from zume.app import SWAPIError, SWAPIException, configure, make_request

configure(app)


class MockResponse(object):

    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


class ViewTest(unittest.TestCase):

    def setUp(self):
        super(ViewTest, self).setUp()
        self.app_context = app.app_context()
        self.app_context.push()

        self.app = app.test_client()
        self.app.application.config["TESTING"] = True

    def tearDown(self):
        super(ViewTest, self).tearDown()

    @patch("requests.get")
    def test_make_request_simple(self, mock):
        mock_resp = MockResponse({"results": []})
        mock.return_value = mock_resp
        resp = make_request("http://foobar.com")
        self.assertIsInstance(resp, dict, "expected dict to be returned")

    @patch("requests.get")
    def test_make_request_network_error(self, mock):
        mock.side_effect = SWAPIException
        with self.assertRaises(SWAPIException):
            make_request("http://foobar.com")

    @patch("requests.get")
    def test_make_request_non_200(self, mock):
        mock.return_value = MockResponse({}, 404)
        with self.assertRaises(SWAPIError):
            make_request("http://foobar.com")

    @patch("requests.get")
    def test_get_films(self, mock):
        mock.return_value = MockResponse({
            "results": [
                {
                    "title": "1",
                    "url": "url/1/",
                    "director": "a"
                },
                {
                    "title": "2",
                    "url": "url/2/",
                    "director": "a"
                },
                {
                    "title": "3",
                    "url": "url/3/",
                    "director": "b"
                },
                {
                    "title": "4",
                    "url": "url/4/",
                    "director": "b"
                },
            ]
        }, 200)
        resp = self.app.get("/films")

        resp = json.loads(resp.data.decode("ascii"))
        self.assertEquals(len(resp.get("a")), 2)
        self.assertEquals(len(resp.get("b")), 2)

    @patch("grequests.imap")
    @patch("requests.get")
    def test_get_characters(self, rmock, gmock):

        rmock.return_value = MockResponse({
            "characters": [
                "http://foobar.com/1",
                "http://foobar.com/2"
            ]
        })

        gmock.side_effect = [
            [
                MockResponse({"name": "Bender"}, 200),
                MockResponse({"name": "Zoidberg"}, 200),
            ]
        ]

        resp = self.app.get("/characters/1")
        resp = json.loads(resp.data.decode("ascii"))

        self.assertEqual(len(resp), 2, "expected two names")
