
import unittest

from datetime import datetime
from xml.etree import ElementTree as ET

from google.appengine.api import users
from restler.serializers import ModelStrategy, to_xml

from tests.models import NdbModel1, NdbModel2


class TestXmlSerialization(unittest.TestCase):

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
            # 'integerlist': [1, 2, 3],
            'user': users.get_current_user(),
            # 'blob': 'binary data',  # TODO
            'text': 'text',
            # 'geopt': ndb.GeoPt("1.0, 2.0"),
            'json_': {'first_name': 'John', 'last_name': 'Smith'}
        }
        self.m.populate(**params)
        self.m.put()

    def tearDown(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()

    def test_alias(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": "text"}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//ndbmodel1")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)
        self.assertEqual(tree.findall(".//the_text")[1].text, 'text')

    def test_change_output(self):
        ss = ModelStrategy(NdbModel1, output_name="person") + [{"the_text": lambda o: o.text}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//person")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)

    def test_property(self):
        ss = ModelStrategy(NdbModel1) + [{"text": lambda o: "the_text"}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//the_text")), 0)

    def test_cached_property(self):
        ss = ModelStrategy(NdbModel2).include('my_cached_property')
        tree = ET.fromstring(to_xml(NdbModel2.query(), ss))
        self.assertEqual(len(tree.findall(".//my_cached_property")), 1)

    def test_json_property(self):
        ss = ModelStrategy(NdbModel1, include_all_fields=True)
        tree = ET.fromstring(to_xml(self.m, ss))
        found = tree.findall(".//json_/first_name")
        self.assertEqual(found[0].text, 'John')
