from django.test import TestCase
from .forms import ItemForm


class TestItemFor(TestCase):

    def test_item_name_is_required(self):
        # simulates a user submitting a form wout a required name
        form = ItemForm({'name': ''})
        # makes the form not valid
        self.assertFalse(form.is_valid())
        # create a dictionary of fields with an error and their associated messages
        self.assertIn('name', form.errors.keys())
        # check to see if the error message on the name fied is'This field is required.'
        self.assertEqual(form.errors['name'][0], 'This field is required.')


    def test_done_field_is_not_required(self):
        form = ItemForm({'name': 'Test Todo Item'})
        self.assertTrue(form.is_valid())

    
    def test_fields_are_explicit_in_form_metaclass(self):
        form = ItemForm()
        self.assertEqual(form.Meta.fields, ['name', 'done'])
