""" Parses the Last.FM events feed """

import urllib
import json
from tornado.httpclient import AsyncHTTPClient

BASE = "http://ws.audioscrobbler.com/2.0/"

class InvalidResults(Exception):
    """ Raised whenever unparseable / error results are returned. """
    pass

class LastFM(object):
    """ Retrieves Last.FM results """

    def __init__(self, api_key, api_secret):
        self.key = api_key
        self.secret = api_secret

    def events(self, callback, location, **params):
        """ Shortcut for geo.getevents method. """
        params['location'] = location
        params.setdefault("limit", 20)
        params.setdefault("method", "geo.getevents")
        def event_callback(response):
            """ Returns LastFMEvent objects """
            events = []
            for event_d in response.get("events", {}).get("event", []):
                event = LastFMEvent.from_json(event_d)
                events.append(event)
            callback(events)
        self.call(event_callback, **params)

    def call(self, callback, **params):
        """ Calls a URL, validates results, and passes to callback """
        client = AsyncHTTPClient()
        params.setdefault("api_key", self.key)
        params.setdefault("format", "json")
        args = urllib.urlencode(params)
        url = "%s?%s" % (BASE, args)
        real_callback = self.wrap(callback)
        return client.fetch(url, callback=real_callback)

    def wrap(self, callback):
        """ Returns a validator which, if valid, calls the real callback. """
        def validate(response):
            """ Checks JSON structure / for errors """
            data = json.loads(response.body)
            if data.get('error'):
                raise InvalidResults(data.get("message", "Error"))
            callback(data)
        return validate

class LastFMEvent(object):
    """ Simpler access for LastFM event data """

    def __init__(self, **params):
        self.id = params.get("id")
        self.title = params.get("title")
        self.artists = params.get("artists")
        self.url = params.get("url")
        self.image = params.get("image")
        self.venue = params.get("venue")

    @classmethod
    def from_json(cls, event):
        """ Extracts data from a JSON event """
        self = cls()
        self.id = event.get("id")
        self.title = event.get("title")
        self.artists = event.get("artists", {}).get("artist", [])
        self.url = event.get("url")
        venue = event.get("venue", {})
        self.venue = venue.get("name")
        self.image = dict([(i.get("size"), i.get("#text"))
                            for i in venue.get("image")]).get("medium")
        return self
