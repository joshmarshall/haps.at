""" The Flickr data feeds """

from haps.libraries.dom import get_text
from haps.views.base import JSONHandler
from torn.route import route
from tornado.web import asynchronous


@route("/feeds/flickr", name="flickr_feed")
class FlickrFeed(JSONHandler):
    """ JSON feed for Flickr Results """

    place = None

    @asynchronous
    def post(self):
        location = self.get_argument("location")
        self.flickr.places.find(self.flickr_geo_callback, query=location)

    def flickr_geo_callback(self, response):
        """ Parses the location and, if valid, starts a photo search. """
        places = response.getElementsByTagName("place")
        if len(places) < 1:
            return self.send_error(400, message="No matching places.")
        place = places[0]
        self.place = place
        place_id = place.getAttribute("place_id")
        place_name = get_text(place)
        per_page = int(self.get_argument("per_page", 20))
        if per_page > 100 or per_page < 10:
            per_page = 20
        self.place = dict(id=place_id, name=place_name)
        self.flickr.photos.search(self.flickr_photos_callback,
                                  place_id=place_id,
                                  per_page=per_page,
                                  media="photos",
                                  content_type=1,
                                  sort="date-posted-desc")

    def flickr_photos_callback(self, response):
        """ Parses the photo results and returns the appropriate
        data. """
        photos = self.flickr.get_photos(response)
        results = dict(entries=[photo.dict() for photo in photos],
                       place=self.place.get("name"))
        self.write(results)
        self.finish()


