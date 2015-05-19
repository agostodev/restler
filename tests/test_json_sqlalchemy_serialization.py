
import json
import pickle

from datetime import datetime, time, timedelta
from unittest import TestCase

from restler import UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqla_models import Base, Model1, Choice, Poll


class TestUnsupportedTypes(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1(
            binary='\xff\xd8\xff\xe1A\xecExif',
            interval=timedelta(1),
            pickle_type=pickle.dumps([1, 2, 3])
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_binary_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('binary')
            to_json(self.session.query(Model1).all(), strategy)

    def test_interval_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('interval')
            to_json(self.session.query(Model1).all(), strategy)

    def test_large_binary_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('large_binary')
            to_json(self.session.query(Model1).all(), strategy)

    def test_pickle_type_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('pickle_type')
            to_json(self.session.query(Model1).all(), strategy)


class TestLambdaJsonSerialization(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1()
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_lambda(self):
        strategy = self.strategy.include(aggregate=lambda o: '%s, %s' % (o.id, o.string))
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0]['aggregate'], u'%s, %s' % (self.model1.id, self.model1.string))


class TestTypes(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1(
            boolean=True,
            interval=timedelta(1),
            _float=5.5,
            string='A string',
            text='Some text'
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_integer_field(self):
        field = 'id'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_boolean_field(self):
        field = 'boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_date_field(self):
        field = '_date'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d'))

    def test_date_time_field(self):
        field = '_datetime'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d %H:%M:%S'))

    def test_float_field(self):
        field = '_float'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_string_field(self):
        field = 'string'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_text_field(self):
        field = 'text'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_time_field(self):
        field = '_time'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), time.strftime(getattr(self.model1, field), '%H:%M:%S'))


class TestRelationships(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.choices = ('Not much', 'The sky', 'Just hacking around')
        poll = Poll(question="What's new?", pub_date=datetime.now())
        self.session.add(poll)

        poll.choices.append(Choice(choice=self.choices[0], votes=0))
        poll.choices.append(Choice(choice=self.choices[1], votes=0))
        poll.choices.append(Choice(choice=self.choices[2], votes=0))
        self.session.commit()

        def choices(poll):
            return [choice for choice in poll.choices]

        poll_strategy = ModelStrategy(Poll, include_all_fields=True).include(choices=choices)
        choice_strategy = ModelStrategy(Choice, include_all_fields=True)
        self.poll_choice_strategy = poll_strategy + choice_strategy

    def test_poll_with_choices(self):
        sj = json.loads(to_json(self.session.query(Poll).all(), self.poll_choice_strategy))
        serialized_choices = [choice.get('choice') for choice in sj[0].get('choices')]
        for choice in serialized_choices:
            self.assertIn(choice, self.choices)
