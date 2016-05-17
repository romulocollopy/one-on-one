import mock
from django.test import TestCase
from project.core.forms import OneOnOneForm


class OneOnOneFormTestCase(TestCase):

    def test_valid_form(self):
        valid_data = {'boby_pk': '1', 'buddy_pk': '3'}
        form = OneOnOneForm(valid_data)
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_in_valid_form(self):
        invalid_data = {'boby_pk': 'um', 'buddy_pk': '3'}
        form = OneOnOneForm(invalid_data)
        valid = form.is_valid()
        self.assertFalse(valid)

    @mock.patch('project.core.forms.BobyRelation')
    def test_form_save_objects(self, BobyRelation):
        valid_data = {'boby_pk': 1, 'buddy_pk': 3}
        form = OneOnOneForm()
        form.cleaned_data = valid_data
        BobyRelation.update_relation.called_once_with(**valid_data)
        form.save_object()

