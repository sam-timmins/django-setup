from django.test import TestCase
from .models import Item


class TestModels(TestCase):

    def test_done_defaults_to_false(self):
        """
        Test the Todo items are created by default with done set to False
        """
        item = Item.objects.create(name='Test Todo item')
        self.assertFalse(item.done)


    def test_items_string_method_returns_name(self):
        item = Item.objects.create(name='Test Todo Item')
        self.assertEqual(str(item), 'Test Todo Item')
