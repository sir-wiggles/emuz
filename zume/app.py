from collections import defaultdict

import requests
from flask import Response, jsonify
from werkzeug.exceptions import HTTPException

import grequests

SWAPI = "https://swapi.co/api"


class SWAPIException(HTTPException):
    code = 503
    description = "SWAPI appears to be down at the moment"


class SWAPIError(HTTPException):
    code = 400
    description = "Unexpected response from SWAPI"


class JsonResponse(Response):

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        elif isinstance(rv, list):
            rv = jsonify(rv)
        elif isinstance(rv, HTTPException):
            rv = jsonify({
                "error": rv.description
            })
        return super(JsonResponse, cls).force_type(rv, environ)


def make_request(url):
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise SWAPIException
    else:
        if resp.status_code != 200:
            raise SWAPIError
    return resp.json()


def configure(app):
    app.response_class = JsonResponse

    @app.errorhandler(Exception)
    def errorhandler(e):
        app.logger.exception(e)
        return {
            "error": "internal server error"
        }, 500

    @app.route("/films", methods=["GET"])
    def get_films():
        group = defaultdict(list)

        resp = make_request("{}/films".format(SWAPI))
        films = resp.get("results", [])

        for film in films:
            item = {
                "title": film["title"],
                "swapi_id": film["url"].split("/")[-2],
            }
            group[film["director"]].append(item)

        return group, 200

    @app.route("/characters/<int:film_id>", methods=["GET"])
    def get_characters(film_id):

        resp = make_request("{}/films/{}".format(SWAPI, film_id))
        urls = resp.get("characters", [])

        names = []
        characters = grequests.imap([grequests.get(url) for url in urls])
        for character in characters:
            if character.status_code != 200:
                continue
            name = character.json().get("name")
            if name is not None:
                names.append(name)

        return names, 200

    return app
