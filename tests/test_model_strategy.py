import unittest

from restler.serializers import ModelStrategy
from tests.models import Model1


class ModelStrategyTest(unittest.TestCase):
    def test_empty_strategy(self):
        ms = ModelStrategy(Model1)
        self.assertEqual(len(ms._ModelStrategy__name_map()), 0)

    def test_all_strategy(self):
        ms = ModelStrategy(Model1, include_all_fields=True)
        self.assertEqual(len(ms.fields), 24)

    def test_one_field_strategy(self):
        ms = ModelStrategy(Model1) + ["string"]
        self.assertEqual(len(ms.fields), 1)

    def test_remove_noexistant_field(self):
        def non_existant_field():
            ModelStrategy(Model1) - ["new_field"]
        self.assertRaises(ValueError, non_existant_field)

    def test_new_instance(self):
        m1 = ModelStrategy(Model1)
        self.assertNotEqual(m1 + ["string"], m1 + ["string"])

    def test_remove_field(self):
        self.assertEqual(
            len(ModelStrategy(Model1, True).fields) - 1,
            len((ModelStrategy(Model1, True) - ["rating"]).fields))

    def test_add_remove_property(self):
        self.assertEqual(len(((ModelStrategy(Model1) + [{"prop": lambda o: o.rating}]) - ["prop"]).fields), 0)

    def test_overridine_field(self):
        self.assertTrue(callable(((ModelStrategy(Model1) + ["rating"]) << [{"rating": lambda o: o.rating}]).fields[0][1]))
