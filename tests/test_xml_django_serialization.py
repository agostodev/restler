from env_setup import setup_django; setup_django()

from unittest import TestCase

from datetime import datetime, time
from xml.etree import ElementTree as ET

from restler.serializers import ModelStrategy, to_xml
from tests.django_models import connection, install_model, Model1


class TestDjangoFieldJsonSerialization(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1(
            big_integer=1,
            boolean=True,
            char="2",
            comma_separated_int=[2, 4, 6],
            decimal=9,
            email='test@domain.com',
            _float=9.5,
            integer=4,
            ip_address='8.8.1.1.',
            null_boolean=None,
            positive_int=100,
            positive_small_int=1,
            slug='Slug Field',
            small_int=1,
            text='More Text',
            url='www.google.com'
        )
        self.model1.save()
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_auto_field(self):
        field = 'id'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_big_integer_field(self):
        field = 'big_integer'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_boolean_field(self):
        field = 'boolean'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_char_field(self):
        field = 'char'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_comma_separated_integer_field(self):
        field = 'comma_separated_int'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s//item' % field)
        for item in found:
            self.assertIn(int(item.text), getattr(self.model1, field))

    def test_date_field(self):
        field = '_date'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, datetime.strftime(getattr(self.model1, field), '%Y-%m-%d'))

    def test_datetime_field(self):
        field = '_datetime'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, datetime.strftime(getattr(self.model1, field), '%Y-%m-%d %H:%M:%S'))

    def test_email_field(self):
        field = 'email'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_float_field(self):
        field = '_float'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_integer_field(self):
        field = 'integer'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_ip_address_field(self):
        field = 'ip_address'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_null_boolean_field(self):
        field = 'null_boolean'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_positive_integer_field(self):
        field = 'positive_int'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_positive_small_integer_field(self):
        field = 'positive_small_int'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_slug_field(self):
        field = 'slug'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_small_integer_field(self):
        field = 'small_int'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, str(getattr(self.model1, field)))

    def test_text_field(self):
        field = 'text'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))

    def test_time_field(self):
        field = '_time'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, time.strftime(getattr(self.model1, field), '%H:%M:%S'))

    def test_url_field(self):
        field = 'url'
        strategy = self.strategy.include(field)
        tree = ET.fromstring(to_xml(Model1.objects.get(pk=self.model1.id), strategy))
        found = tree.findall('.//%s' % field)
        self.assertEqual(found[0].text, getattr(self.model1, field))
