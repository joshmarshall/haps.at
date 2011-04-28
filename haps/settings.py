"""
This file contains all of the default settings for your app.
You should add anything "default" parameters (i.e. dummy api keys,
local database connection information, etc.) in this file, but
for deployment specific options, you should create a settings_local.py
file and overwrite the changes.
"""

from torn.config import load_settings
from os.path import join, dirname, abspath

settings = load_settings(dict(

    # Add your settings here
    port = 8000,
    address = "",
    debug = True,
    cookie_secret = "^o-p^!!l3nm)qi3pl!)@a2s#_t318s@y_+f0#rhy)z#wp%fh+x",
    xsrf_cookies = True,
    static_path = abspath(join(dirname(__file__), "../static")),
    template_path = abspath(join(dirname(__file__), "../templates")),

    # Flickr API information
    flickr_api_key = "OVERWRITE IN settings_local.py",
    flickr_api_secret = "OVERWRITE IN settings_local.py",

    # Twitter API information
    twitter_consumer_key = "OVERWRITE IN settings_local.py",
    twitter_consumer_secret = "OVERWRITE IN settings_local.py",

    # LastFM API information
    lastfm_api_key = "OVERWRITE IN settings_local.py",
    lastfm_api_secret = "OVERWRITE IN settings_local.py",

    # Yelp API Information
    yelp_api_key =  "OVERWRITE IN settings_local.py",

))
