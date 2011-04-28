""" The Twitter data feeds """

from haps.views.base import JSONHandler
from torn.route import route
from tornado.web import asynchronous
from tornado.auth import TwitterMixin
from tornado.httpclient import AsyncHTTPClient
import urllib
import json

@route("/feeds/twitter", name="twitter_feed")
class TwitterFeed(JSONHandler, TwitterMixin):
    """ Retrieves Tweets from a specific location """

    @asynchronous
    def post(self):
        location = self.get_argument("location")
        self.twitter_request("/geo/search",
                             query=location,
                             callback=self.twitter_geo_callback)

    def twitter_geo_callback(self, response):
        """ Parses for a place_id, and searches for tweets if found """
        places = response.get('result', {}).get('places', [])
        if not places:
            return self.send_error(400, message="Not a recognized place.")
        # Assuming first place
        place = places[0]
        self.place = place
        place_id = place['id']
        args = urllib.urlencode(dict(q="place:%s" % place_id,
                                     result_type="mixed"))
        search_url = "http://search.twitter.com/search.json?%s" % args
        client = AsyncHTTPClient()
        client.fetch(search_url, self.twitter_tweets_callback)

    def twitter_tweets_callback(self, response):
        """ Parses the response data and returns simplified results. """
        data = json.loads(response.body)
        results = data.get('results', [])
        final_results = []
        for result in results:
            username = result.get("from_user")
            image = result.get("profile_image_url")
            created = result.get("created_at")
            text = result.get("text")
            place = result.get("place", {}).get("name")
            final_results.append(dict(username=username,
                                      image=image,
                                      created=created,
                                      text=text,
                                      place=place))
        self.write(dict(entries=final_results,
                        place=self.place.get('full_name')))
        self.finish()
