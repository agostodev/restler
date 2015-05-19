import unittest

from restler import models


class RequiredTransientModel(models.TransientModel):
    @classmethod
    def required_fields(cls):
        return ('sku', 'model_number')


class OptionalTransientModel(models.TransientModel):
    @classmethod
    def optional_fields(cls):
        return ('short_description', 'long_description')


class MixedTransientModel(models.TransientModel):
    @classmethod
    def required_fields(cls):
        return ('sku', 'model_number')

    @classmethod
    def optional_fields(cls):
        return ('short_description', 'long_description')


class TransientModelTest(unittest.TestCase):

    def test_required_fields(self):
        self.assertEqual(('sku', 'model_number'), RequiredTransientModel.required_fields())
        self.assertEqual(tuple(), OptionalTransientModel.required_fields())
        self.assertEqual(('sku', 'model_number'), MixedTransientModel.required_fields())

    def test_optional_fields(self):
        self.assertEqual(tuple(), RequiredTransientModel.optional_fields())
        self.assertEqual(('short_description', 'long_description'), OptionalTransientModel.optional_fields())
        self.assertEqual(('short_description', 'long_description'), MixedTransientModel.optional_fields())

    def test_fields(self):
        self.assertEqual(('sku', 'model_number'), RequiredTransientModel.fields())
        self.assertEqual(('short_description', 'long_description'), OptionalTransientModel.fields())
        self.assertEqual(('sku', 'model_number', 'short_description', 'long_description'), MixedTransientModel.fields())

    def test_constructor_required(self):
        with self.assertRaises(AttributeError) as context:
            RequiredTransientModel(model_number='12345')
        self.assertEqual('The property: sku is required.', context.exception[0])
        with self.assertRaises(AttributeError) as context:
            RequiredTransientModel(sku='98765')
        self.assertEquals('The property: model_number is required.', context.exception[0])
        subject = RequiredTransientModel(
            sku='98765',
            model_number='12345'
        )
        self.assertEqual('98765', subject.sku)
        self.assertEqual('12345', subject.model_number)

    def test_contructor_optional(self):
        empty_subject = OptionalTransientModel()
        self.assertIs(None, empty_subject.short_description)
        self.assertIs(None, empty_subject.long_description)
        full_subject = OptionalTransientModel(
            short_description='a terse description',
            long_description='a much more wordy description'
        )
        self.assertEqual('a terse description', full_subject.short_description)
        self.assertEqual('a much more wordy description', full_subject.long_description)

    def test_constructor_mixed(self):
        with self.assertRaises(AttributeError) as context:
            MixedTransientModel(
                model_number='12345',
                short_description='a terse description',
                long_description='a much more wordy description'
            )
        self.assertEqual('The property: sku is required.', context.exception[0])
        with self.assertRaises(AttributeError) as context:
            MixedTransientModel(
                sku='98765',
                short_description='a terse description',
                long_description='a much more wordy description'
            )
        self.assertEquals('The property: model_number is required.', context.exception[0])
        partial_subject = MixedTransientModel(
            sku='98765',
            model_number='12345'
        )
        self.assertEqual('98765', partial_subject.sku)
        self.assertEqual('12345', partial_subject.model_number)
        self.assertIs(None, partial_subject.short_description)
        self.assertIs(None, partial_subject.long_description)
        full_subject = MixedTransientModel(
            sku='98765',
            model_number='12345',
            short_description='a terse description',
            long_description='a much more wordy description'
        )
        self.assertEqual('98765', full_subject.sku)
        self.assertEqual('12345', full_subject.model_number)
        self.assertEqual('a terse description', full_subject.short_description)
        self.assertEqual('a much more wordy description', full_subject.long_description)

    def test_properties(self):
        partial_subject = MixedTransientModel(
            sku='98765',
            model_number='12345'
        )
        self.assertEqual({
            'sku': '98765',
            'model_number': '12345',
            'short_description': None,
            'long_description': None
        }, partial_subject.properties())
        full_subject = MixedTransientModel(
            sku='98765',
            model_number='12345',
            short_description='a terse description',
            long_description='a much more wordy description'
        )
        self.assertEqual({
            'sku': '98765',
            'model_number': '12345',
            'short_description': 'a terse description',
            'long_description': 'a much more wordy description'
        }, full_subject.properties())
