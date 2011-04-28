""" This is the BaseHandler. All other Handlers should extend it. """

from torn.base import Handler
from haps.libraries.lastfm import LastFM
from haps.libraries.flickr import Flickr
from haps.libraries.yelp import Yelp
from haps.settings import settings
import httplib

class BaseHandler(Handler):
    """ The most basic of handlers. """

    _flickr = None
    _lastfm = None
    _yelp = None

    @property
    def flickr(self):
        """ Just a request-level 'singleton' for the Flickr API """
        if not self._flickr:
            self._flickr = Flickr(settings.flickr_api_key,
                                  settings.flickr_api_secret)
        return self._flickr

    @property
    def lastfm(self):
        """ Just a request-level 'singleton' for the LastFM API """
        if not self._lastfm:
            self._lastfm = LastFM(settings.lastfm_api_key,
                                  settings.lastfm_api_secret)
        return self._lastfm

    @property
    def yelp(self):
        """ Just a request-level 'singleton' for the Yelp API """
        if not self._yelp:
            self._yelp = Yelp(settings.yelp_api_key)
        return self._yelp

class JSONHandler(BaseHandler):
    """ A few helper methods for JSON results, plus overwriting the
    send_error and get_error_html methods. """

    def send_error(self, status_code=500, **kwargs):
        self.set_status(status_code)
        self.set_header("Content-type", "application/json")
        response_message = httplib.responses[status_code]
        self.write(dict(status="error",
                        code=status_code,
                        message=kwargs.get("message", response_message)))
        self.finish()
