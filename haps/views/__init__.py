"""
This file sets up what routes are used by the server. You
should import any modules in this directory that you want
to have accessible to the application, and then call the
route.get_routes() method as shown below.
"""

# Import all the views you want to utilize
import haps.views.index
import haps.views.feeds.flickr
import haps.views.feeds.twitter
import haps.views.feeds.lastfm
import haps.views.feeds.yelp

# After all views are imported...
from torn.route import route
routes = route.get_routes()
