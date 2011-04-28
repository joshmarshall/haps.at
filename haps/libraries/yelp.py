""" Implements Yelp's Neighborhood Review lookup (v1) """

from tornado.httpclient import AsyncHTTPClient
import json
import urllib

BASE = "http://api.yelp.com"

class InvalidRequest(Exception):
    """ Raised in case of error response """
    pass

class Yelp(object):
    """ Search Yelp's feeds and return results. """

    def __init__(self, api_key):
        self.key = api_key

    def call(self, callback, path, **params):
        """ Fetch a result and validate before calling callback """
        client = AsyncHTTPClient()
        params.setdefault("ywsid", self.key)
        args = urllib.urlencode(params)
        url = "%s%s?%s" % (BASE, path, args)
        return client.fetch(url, callback=self.wrap(callback))

    def search(self, callback, **params):
        """ Does a business review search """
        path = "/business_review_search"
        def result_callback(data):
            """ Returns a list of YelpPlace(s) """
            results = []
            for result in data.get("businesses", []):
                results.append(result)
            callback(results)
        return self.call(result_callback, path, **params)

    def wrap(self, callback):
        """ Wraps the callback with a validation function """
        def validate(response):
            """ Checks JSON structure for errors and passes to callback """
            data = json.loads(response.body)
            message = data.get("message", {})
            if message and message.get("code") != 0:
                raise InvalidRequest(message.get("text", "Invalid request"))
            callback(data)
        return validate
