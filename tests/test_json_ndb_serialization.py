import json
import pickle
import unittest

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

from restler import UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json, SKIP

from tests.helpers import flip
from tests.models import NdbModel1, NdbModel2, NdbModel3


MODEL1 = {
    u'string': u'string',
    u'stringlist': [u'one', u'two', u'three'],
    u'text': u'text',
    u'float_': 22.0, u'blob': u'binary data',
    u'geopt': u'1.0 2.0', u'boolean': True,
    u'integer': 123,
    u'integerlist': [1, 2, 3],
    u'user': None,
    u'json_': {u'first_name': u'John', u'last_name': u'Smith'}
}


class TestJsonSerialization(unittest.TestCase):

    def setUp(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()
        ref = NdbModel1()
        ref.put()
        m2 = NdbModel2()
        m2.put()

        self.m = NdbModel1()
        params = {
            'string': 'string',
            'boolean': True,
            'integer': 123,
            'float_': 22.0,
            'datetime': datetime.now(),
            'date': datetime.now().date(),
            'time': datetime.now().time(),
            'stringlist': ['one', 'two', 'three'],
            'integerlist': [1, 2, 3],
            'user': users.get_current_user(),
            'blob': 'binary data',  # TODO
            'text': 'text',
            'geopt': ndb.GeoPt("1.0, 2.0"),
            'json_': {'first_name': 'John', 'last_name': 'Smith'}
        }
        self.m.populate(**params)
        self.m.put()
        self.all_model1 = NdbModel1.query().order(-NdbModel1.datetime)

    def tearDown(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()

    def test_nomodel(self):
        self.assertEqual(flip({'success': True}), {"success": True})

    def test_simple(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": "text"}]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0], {u'the_text': u'text'})

    def test_simple_property(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": lambda o: o.text}]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0], {u'the_text': u'text'})

    def test_exclude_fields(self):
        ss = ModelStrategy(NdbModel1, include_all_fields=True) - ["date", "time", "datetime"]
        sj = json.loads(to_json(self.all_model1, ss))
        self.assertEqual(sj[0], MODEL1)

    def test_valid_serialization(self):
        ss = ModelStrategy(NdbModel1, include_all_fields=True) - ["date", "time", "datetime"]
        dict_data = {'foo': 'foo', 'models': self.all_model1}
        sj = json.loads(to_json(dict_data, ss))
        self.assertEqual(sj['models'][0], MODEL1)

    def test_alias_field(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + [{"my_method": "my_method"}]),
            {"my_method": "I say blah!"})

    def test_alias_field2(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + ["my_method"]),
            {"my_method": "I say blah!"})

    def test_alias_field3(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2)
            + [{"my_method": lambda obj, context: context["foo"]}], context={"foo": "woohoo"}),
            {"my_method": "woohoo"})

    def test_alias_field4(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + [{"yes": lambda o: "yes"}, {"no": lambda o: SKIP}]),
            {"yes": "yes"})

    def test_cached_property(self):
        ss = ModelStrategy(NdbModel2).include('my_cached_property')
        sj = json.loads(to_json(NdbModel2.query(), ss))
        self.assertEqual(sj[0], {u'my_cached_property': u'my cached property'})

    def test_json_property(self):
        ss = ModelStrategy(NdbModel1).include('json_')
        json_str = to_json(self.m, ss)
        self.assertEqual(json_str, '{"json_": {"first_name": "John", "last_name": "Smith"}}')
        sj = json.loads(json_str)
        self.assertEqual(sj, {u'json_': {u'first_name': u'John', u'last_name': u'Smith'}})


class TestNdbUnsupportedFields(unittest.TestCase):
    def setUp(self):
        for e in NdbModel3.query():
            e.key.delete()

        model = NdbModel3(generic='generic property', name='Smith', pickle_=pickle.dumps([1, 2]))
        model.put()
        self.strategy = ModelStrategy(NdbModel3, include_all_fields=False)

    def test_generic_property_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('generic')
            to_json(NdbModel3.query(), strategy)

    def test_computed_property_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('name_lower')
            to_json(NdbModel3.query(), strategy)

    def test_pickle_property_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('pickle_')
            to_json(NdbModel3.query(), strategy)
