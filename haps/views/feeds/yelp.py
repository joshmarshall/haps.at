""" The LastFM events feed """

from tornado.web import asynchronous
from torn.route import route
from haps.views.base import JSONHandler

@route("/feeds/yelp", name="yelp_feed")
class YelpFeed(JSONHandler):
    """ Retrieves events from LastFM and returns JSON """

    @asynchronous
    def post(self):
        location = self.get_argument("location")
        self.yelp.search(self.yelp_places_callback,
                         term="food",
                         location=location)

    def yelp_places_callback(self, results):
        """ Parses the results and returns a simplified dictionary """
        final_results = []
        for result in results:
            place = dict(name=result.get("name"),
                         image=result.get("photo_url"),
                         url=result.get("url"),
                         rating_image=result.get("rating_img_url"))
            final_results.append(place)
        self.write(dict(entries=final_results))
        self.finish()

