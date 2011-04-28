""" This client implements the Flickr API """

import xml.dom.minidom
import urllib
from tornado.httpclient import AsyncHTTPClient

BASE = "http://api.flickr.com/services/rest/"

class Flickr(object):
    """ Implements the basics of the Flickr API. No auth or
    anything spectacularly cool yet, mostly for the public
    feeds.
    """

    def __init__(self, api_key, api_secret):
        self.key = api_key
        self.secret = api_secret

    def call(self, callback, method, **params):
        """ Forms the final URL and calls it. """
        cb_wrapped = self.wrap(callback)
        client = AsyncHTTPClient()
        params.setdefault("api_key", self.key)
        params['method'] = method
        args = urllib.urlencode(params)
        # Do auth-signing stuff here
        url = "%s?%s" % (BASE, args)
        return client.fetch(url, cb_wrapped)

    def wrap(self, func):
        """ 'Wraps' a function with the Flickr body validator. """
        def callback(response):
            """ Parses / validates the response, and passes it
            to the original callback.
            """
            result = validate(response.body)
            func(result)
        return callback

    def get_photos(self, response):
        """ Retrieves a list of FlickrPhoto's from a DOM response """
        photos = response.getElementsByTagName("photo")
        results = []
        for photo in photos:
            results.append(FlickrPhoto.from_photo_entry(photo))
        return results

    def __getattr__(self, name):
        """ Shortcut to the method calls -- we'll need to limit
        this at some point. """
        return FlickrMethodNS(self, "flickr.%s" % name)

class FlickrMethodNS(object):
    """ Just a helper to make dot-namespaces work. """
    def __init__(self, api, namespace='flickr'):
        self._namespaces = [namespace,]
        self._api = api

    def __getattr__(self, name):
        """ Appends to namespace and returns self """
        self._namespaces.append(name)
        return self

    def __call__(self, callback_fn, **params):
        """ Just wraps the API call() method. """
        method = '.'.join(self._namespaces)
        params.setdefault('method', method)
        return self._api.call(callback_fn, **params)

QUALITY_MAP = dict(thumb="_t", square="_s", medium="",
                   large="_b", small="_m")

class FlickrPhoto(object):
    """ Just a simple object for accessing photo stuff """

    def __init__(self, **params):
        self.id = params.get("id")
        self.owner = params.get("owner")
        self.secret = params.get("secret")
        self.farm = params.get("farm")
        self.server = params.get("server")
        self.title = params.get("title")

    @classmethod
    def from_photo_entry(cls, entry):
        """ Parses a <photo> dom element and populates the object """
        self = cls()
        self.id = entry.getAttribute("id")
        self.secret = entry.getAttribute("secret")
        self.farm = entry.getAttribute("farm")
        self.server = entry.getAttribute("server")
        self.owner = entry.getAttribute("owner")
        self.title = entry.getAttribute("title")
        return self

    def image(self, quality="z", **params):
        """ Returns a particular quality level """
        if QUALITY_MAP.get(quality) != None:
            quality = QUALITY_MAP.get(quality)
        params.setdefault("id", self.id)
        params.setdefault("farm", self.farm)
        params.setdefault("server", self.server)
        params.setdefault("secret", self.secret)
        params.setdefault("quality", quality)
        base = "http://farm%(farm)s.static.flickr.com/"+\
               "%(server)s/%(id)s_%(secret)s%(quality)s.jpg"
        return base % params

    def dict(self):
        """ Just returns a dictionary of the main attributes. """
        doc = dict(id=self.id,
                   title=self.title,
                   images=dict([(k, self.image(k))
                                for k in QUALITY_MAP.keys()]))
        return doc

class FlickrError(Exception):
    """ Used when an error response is returned from a Flickr request. """
    pass

def validate(body):
    """ Loads DOM, and checks for errors. """
    dom = xml.dom.minidom.parseString(body)
    response = dom.getElementsByTagName("rsp")
    if len(response) != 1:
        raise FlickrError("Invalid response format.")
    response = response[0]
    status = response.getAttribute("stat")
    error = response.getElementsByTagName("err")
    if status == "fail":
        error = error[0]
        code = error.getAttribute("code")
        message = error.getAttribute("msg")
        raise FlickrError("%s - %s" % (code, message))
    return response
