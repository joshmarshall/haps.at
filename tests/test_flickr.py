""" Tests the Flickr methods """

from haps.libraries.flickr import Flickr, validate, FlickrError
from haps.libraries.flickr import FlickrMethodNS, FlickrPhoto, QUALITY_MAP
import xml.dom.minidom
import unittest

VALID_RESPONSE = '<?xml version="1.0" encoding="utf-8" ?><rsp stat="ok">'+\
                 '<photos page="1" pages="100" perpage="250" total="25000">'+\
                 '<photo id="5555555555" owner="4444444@N44" '+\
                 'secret="ca14774fed" server="5264" farm="6" '+\
                 'title="Photo!" ispublic="1" isfriend="0" isfamily="0" />'+\
                 '</photos></rsp>'

INVALID_RESPONSE = '<?xml version="1.0" encoding="utf-8" ?>'+\
                   '<rsp stat="fail"><err code="100" '+\
                   'msg="Invalid API Key (Key has invalid format)" />'+\
                   '</rsp>'

VALID_PHOTO = '<photo id="foo" owner="bar" secret="baz" server="hal" '+\
              'farm="beet" title="reynolds" ispublic="1" isfriend="0" '+\
              'isfamily="0" />'

class TestFlickrValidation(unittest.TestCase):
    """ Tests the validate function """

    def test_valid(self):
        """ Test a valid response """
        result = validate(VALID_RESPONSE)
        self.assertTrue(result.getAttribute('stat') == 'ok')

    def test_error(self):
        """ Test an invalid response """
        self.assertRaises(FlickrError, validate, INVALID_RESPONSE)


    def test_wrapped(self):
        """ Test the API wrap method. """
        api = Flickr('none', 'none')
        result = dict(error=True)
        class Response(object):
            """ Fake response object """
            def __init__(self, body):
                self.body = body

        def callback(response):
            """ Test callback """
            self.assertTrue(response.getAttribute('stat') == 'ok')
            result['error'] = False
        func = api.wrap(callback)
        func(Response(VALID_RESPONSE))
        self.assertFalse(result['error'])


class TestMethodNS(unittest.TestCase):
    """ Tests the Flickr method dot-name shortcut """

    def setUp(self):
        class Fixture(object):
            """ Fake Flickr object """
            def call(self, callback, **params):
                """ Make the 'fake' call """
                callback(params)
        self.fixture = Fixture()

    def test_class(self):
        """ Test the FlickrMethodNS object """
        result = dict(error=True)
        methodns = FlickrMethodNS(self.fixture, "test")
        def callback(params):
            """ Updates result with parameters """
            result['error'] = False
            result.update(params)

        methodns.really.longish.namespace(callback, foo="bar")
        self.assertTrue(result == dict(error=False, foo="bar",
                                       method="test.really.longish.namespace"))

class TestFlickrPhoto(unittest.TestCase):
    """ Tests the FlickrPhoto methods. """

    def test_init(self):
        """ Test the FlickrPhoto __init__ params """
        photo = FlickrPhoto(id="foo", owner="bar",
                            secret="baz", server="hal",
                            farm="beet", title="reynolds")
        self.assert_photo(photo)

    def assert_photo(self, photo):
        """ Asserts for the photos attributes """
        base = "http://farmbeet.static.flickr.com/hal/foo_baz%s.jpg"
        self.assertTrue(photo.id == "foo")
        self.assertTrue(photo.owner == "bar")
        self.assertTrue(photo.secret == "baz")
        self.assertTrue(photo.server == "hal")
        self.assertTrue(photo.farm == "beet")
        self.assertTrue(photo.title == "reynolds")
        for key, val in QUALITY_MAP.iteritems():
            image = photo.image(key)
            hypothesis = base % val
            self.assertTrue(image == hypothesis)

    def test_from_photo_entry(self):
        """ Test the FlickrPhoto from_photo_entry() method """
        dom = xml.dom.minidom.parseString(VALID_PHOTO).firstChild
        photo = FlickrPhoto.from_photo_entry(dom)
        self.assert_photo(photo)

