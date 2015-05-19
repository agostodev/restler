from env_setup import setup_django; setup_django()

import json

from datetime import datetime, time
from unittest import TestCase

from restler import UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json

from tests.django_models import connection, install_model, Model1, Poll, Choice


class TestDjangoUnsupportedFields(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1()
        self.model1.save()
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_file_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('_file')
            to_json(Model1.objects.all(), strategy)

    def test_file_path_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('file_path')
            to_json(Model1.objects.all(), strategy)

    def test_image_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('image')
            to_json(Model1.objects.all(), strategy)


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
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_big_integer_field(self):
        field = 'big_integer'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_boolean_field(self):
        field = 'boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_char_field(self):
        field = 'char'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_comma_separated_integer_field(self):
        field = 'comma_separated_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_date_field(self):
        field = '_date'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d'))

    def test_datetime_field(self):
        field = '_datetime'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d %H:%M:%S'))

    def test_decimal_field(self):
        field = 'decimal'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), str(getattr(self.model1, field)))

    def test_email_field(self):
        field = 'email'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_float_field(self):
        field = '_float'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_integer_field(self):
        field = 'integer'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_ip_address_field(self):
        field = 'ip_address'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_null_boolean_field(self):
        field = 'null_boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_positive_integer_field(self):
        field = 'positive_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_positive_small_integer_field(self):
        field = 'positive_small_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_slug_field(self):
        field = 'slug'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_small_integer_field(self):
        field = 'small_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_text_field(self):
        field = 'text'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_time_field(self):
        field = '_time'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), time.strftime(getattr(self.model1, field), '%H:%M:%S'))

    def test_url_field(self):
        field = 'url'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))


class TestLambdaJsonSerialization(TestCase):
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
        self.strategy = ModelStrategy(Model1, include_all_fields=True).exclude('_file', 'file_path', 'image')

    def test_lambda(self):
        strategy = self.strategy.include(aggregate=lambda o: '%s, %s' % (o.big_integer, o.char))
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get('aggregate'), u'1, 2')


class TestRelationships(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Poll)
        install_model(Choice)

        self.choices = ('Not much', 'The sky', 'Just hacking around')
        poll = Poll(question="What's new?", pub_date=datetime.now())
        poll.save()
        poll.choice_set.create(choice=self.choices[0], votes=0)
        poll.choice_set.create(choice=self.choices[1], votes=0)
        poll.choice_set.create(choice=self.choices[2], votes=0)
        poll.save()

        def choices(poll):
            return [choice for choice in poll.choice_set.all()]

        poll_strategy = ModelStrategy(Poll, include_all_fields=True).include(choices=choices)
        choice_strategy = ModelStrategy(Choice, include_all_fields=True)
        self.poll_choice_strategy = poll_strategy + choice_strategy

    def test_poll_with_choices(self):
        sj = json.loads(to_json(Poll.objects.all(), self.poll_choice_strategy))
        serialized_choices = [choice.get('choice') for choice in sj[0].get('choices')]
        for choice in serialized_choices:
            self.assertIn(choice, self.choices)
