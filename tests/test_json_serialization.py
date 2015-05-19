
import json
import unittest

from datetime import datetime
from google.appengine.api import users
from restler.serializers import ModelStrategy, to_json, SKIP

from tests.models import Model1, Model2


def flip(*args, **kwargs):
    return json.loads(to_json(*args, **kwargs))


class TestJsonSerialization(unittest.TestCase):

    def setUp(self):
        for e in Model1.all():
            e.delete()
        for e in Model2.all():
            e.delete()
        ref = Model1()
        ref.put()
        m = Model1()
        m2 = Model2()
        m2.put()
        m.string = "string"
        m.bytestring = "\00\0x"
        m.boolean = True
        m.integer = 123
        m.float_ = 22.0
        m.datetime = datetime.now()
        m.date = datetime.now().date()
        m.time = datetime.now().time()
        m.list_ = [1, 2, 3]
        m.stringlist = ["one", "two", "three"]
        m.reference = m2
        m.selfreference = ref
        m.blobreference = None  # Todo
        m.user = users.get_current_user()
        m.blob = "binary data"  # Todo
        m.text = "text"
        m.category = "category"
        m.link = "http://www.yahoo.com"
        m.email = "joe@yahoo.com"
        m.geopt = "1.0, 2.0"
        m.im = "http://aim.com/ joe@yahoo.com"
        m.phonenumber = "612-292-4339"
        m.postaladdress = "234 Shady Oak Rd., Eden Prairie, MN, 55218"
        m.rating = 23
        m.put()
        self.all_model1 = Model1.all().order("-datetime")

    def tearDown(self):
        for e in Model1.all():
            e.delete()
        for e in Model2.all():
            e.delete()

    def test_nomodel(self):
        self.assertEqual(flip({'success': True}), {"success": True})

    def test_simple(self):
        ss = ModelStrategy(Model1) + [{"the_text": "text"}]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0], {u'the_text': u'text'})

    def test_simple_property(self):
        ss = ModelStrategy(Model1) + [{"the_text": lambda o: o.text}]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0], {u'the_text': u'text'})

    def test_exclude_fields(self):
        ss = ModelStrategy(Model1, True) - ["date", "time", "datetime"]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0],
            {
                u'category': u'category', u'rating': 23, u'list_': [1, 2, 3],
                u'string': u'string', u'reference': {u'model2_prop': None},
                u'selfreference': {u'category': None, u'rating': None,
                u'list_': [], u'string': None, u'reference': None,
                u'selfreference': None, u'text': None, u'stringlist': [],
                u'blobreference': None, u'float_': None, u'im': None,
                u'blob': None, u'geopt': None, u'boolean': None,
                u'link': None, u'postaladdress': None, u'bytestring': None,
                u'integer': None, u'email': None, u'phonenumber': None,
                u'user': None}, u'text': u'text',
                u'stringlist': [u'one', u'two', u'three'],
                u'blobreference': None, u'float_': 22.0,
                u'im': u'http://aim.com/ joe@yahoo.com',
                u'blob': u'binary data', u'geopt': u'1.0 2.0',
                u'boolean': True, u'link': u'http://www.yahoo.com',
                u'postaladdress': u'234 Shady Oak Rd., Eden Prairie, MN, 55218',
                u'bytestring': u'\x00\x00x', u'integer': 123,
                u'email': u'joe@yahoo.com', u'phonenumber': u'612-292-4339',
                u'user': None
            }
        )

    def test_valid_serialization(self):
        ss = ModelStrategy(Model1, include_all_fields=True) - ["date", "time", "datetime"]
        dict_data = {'foo': 'foo', 'models': self.all_model1}
        sj = json.loads(to_json(dict_data, ss))
        self.assertEqual(sj['models'][0],
            {
                u'category': u'category', u'rating': 23, u'list_': [1, 2, 3], u'string': u'string',
                u'reference': {u'model2_prop': None},
                u'selfreference': {
                    u'category': None, u'rating': None, u'list_': [], u'string': None,
                    u'reference': None, u'selfreference': None, u'text': None, u'stringlist': [],
                    u'blobreference': None, u'float_': None, u'im': None, u'blob': None, u'geopt': None,
                    u'boolean': None, u'link': None, u'postaladdress': None, u'bytestring': None,
                    u'integer': None, u'email': None, u'phonenumber': None, u'user': None
                },
                u'text': u'text', u'stringlist': [u'one', u'two', u'three'], u'blobreference': None,
                u'float_': 22.0, u'im': u'http://aim.com/ joe@yahoo.com', u'blob': u'binary data',
                u'geopt': u'1.0 2.0', u'boolean': True, u'link': u'http://www.yahoo.com',
                u'postaladdress': u'234 Shady Oak Rd., Eden Prairie, MN, 55218',
                u'bytestring': u'\x00\x00x', u'integer': 123, u'email': u'joe@yahoo.com',
                u'phonenumber': u'612-292-4339', u'user': None
            })

    def test_alias_field(self):
        self.assertEqual(flip(Model2(), ModelStrategy(Model2) + [{"my_method": "my_method"}]),
            {"my_method": "I say blah!"})

    def test_alias_field2(self):
        self.assertEqual(flip(Model2(), ModelStrategy(Model2) + ["my_method"]),
            {"my_method": "I say blah!"})

    def test_alias_field3(self):
        self.assertEqual(flip(Model2(), ModelStrategy(Model2)
            + [{"my_method": lambda obj, context: context["foo"]}], context={"foo": "woohoo"}),
            {"my_method": "woohoo"})

    def test_alias_field4(self):
        self.assertEqual(flip(Model2(), ModelStrategy(Model2) + [{"yes": lambda o: "yes"}, {"no": lambda o: SKIP}]),
            {"yes": "yes"})

    def test_cached_property(self):
        ss = ModelStrategy(Model2).include('my_cached_property')
        sj = json.loads(to_json(Model2.all(), ss))
        self.assertEqual(sj[0], {u'my_cached_property': u'my cached property'})
