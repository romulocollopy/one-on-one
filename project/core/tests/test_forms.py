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
        invalid_data = {'boby_pk': 'um', 'buddy_pk': '3'}
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


class UploadUsersFormTestCase(TestCase):

    def setUp(self):
        self.boby = mock.Mock()
        self.valid_data = {}

    @mock.patch('project.core.forms.rules.test_rule')
    def test_form_is_valid(self, mock_rule):
        mock_rule.return_value = True
        form = UploadUsersForm(self.valid_data)
        form.is_valid(self.boby)
        mock_rule.assert_called_once_with('can_upload_users', self.boby)

    @mock.patch('project.core.forms.rules.test_rule')
    def test_form_raises_permissionerror(self, mock_rule):
        mock_rule.return_value = False
        form = UploadUsersForm(self.valid_data)
        with self.assertRaises(PermissionDenied):
            form.is_valid(self.boby)

    def test_form_save(self):
        form = UploadUsersForm(self.valid_data)
        form.cleaned_data = {}
        form.save()
