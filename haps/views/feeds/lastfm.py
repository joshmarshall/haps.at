""" The LastFM events feed """

from tornado.web import asynchronous
from torn.route import route
from haps.views.base import JSONHandler

@route("/feeds/lastfm", name="lastfm_feed")
class LastFMFeed(JSONHandler):
    """ Retrieves events from LastFM and returns JSON """

    @asynchronous
    def post(self):
        location = self.get_argument("location")
        self.lastfm.events(self.lastfm_events_callback, location)

    def lastfm_events_callback(self, results):
        """ Parses the results and returns a simplified dictionary """
        final_results = []
        for result in results:
            event = dict(title=result.title,
                         image=result.image,
                         artists=result.artists,
                         venue=result.venue)
            final_results.append(event)
        self.write(dict(entries=final_results))
        self.finish()

