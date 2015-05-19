
import unittest

from google.appengine.api import users
from restler.serializers import ModelStrategy, to_xml
from tests.models import Model1, Model2
from datetime import datetime

from xml.etree import ElementTree as ET


class TestXmlSerialization(unittest.TestCase):

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

    def tearDown(self):
        for e in Model1.all():
            e.delete()
        for e in Model2.all():
            e.delete()

    def test_alias(self):
        ss = ModelStrategy(Model1) + [{"the_text": "text"}]
        tree = ET.fromstring(to_xml(Model1.all(), ss))
        self.assertEqual(len(tree.findall(".//model1")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)
        self.assertEqual(tree.findall(".//the_text")[1].text, 'text')

    def test_change_output(self):
        ss = ModelStrategy(Model1, output_name="person") + [{"the_text": lambda o: o.text}]
        tree = ET.fromstring(to_xml(Model1.all(), ss))
        self.assertEqual(len(tree.findall(".//person")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)

    def test_property(self):
        ss = ModelStrategy(Model1) + [{"text": lambda o: "the_text"}]
        tree = ET.fromstring(to_xml(Model1.all(), ss))
        self.assertEqual(len(tree.findall(".//the_text")), 0)

    def test_cached_property(self):
        ss = ModelStrategy(Model2).include('my_cached_property')
        tree = ET.fromstring(to_xml(Model2.all(), ss))
        self.assertEqual(len(tree.findall(".//my_cached_property")), 1)
