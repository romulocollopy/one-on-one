import mock
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from project.core.forms import OneOnOneForm, UploadUsersForm


class OneOnOneFormTestCase(TestCase):

    def setUp(self):
        self.boby = mock.Mock()

    @mock.patch('project.core.forms.BobyRelation')
    def test_valid_form(self, MockRelation):
        valid_data = {'boby_pk': '1', 'buddy_pk': '3'}
        form = OneOnOneForm(valid_data)
        valid = form.is_valid(self.boby)
        self.assertTrue(valid)

    def test_in_valid_form(self):
        invalid_data = {'boby_pk': 'um', 'buddy_pk': '3', 'create_relation': True}
        form = OneOnOneForm(invalid_data)
        valid = form.is_valid(self.boby)
        self.assertFalse(valid)

    @mock.patch('project.core.forms.BobyRelation')
    def test_form_save_objects(self, MockRelation):
        valid_data = {'boby_pk': 1, 'buddy_pk': 3}
        form = OneOnOneForm()
        form.cleaned_data = valid_data
        form.boby = self.boby
        MockRelation.update_relation.called_once_with(self.boby, **valid_data)
        form.save_object()
