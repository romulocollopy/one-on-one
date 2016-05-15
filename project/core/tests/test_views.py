import mock

from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from core.models import Boby


class TestViewsMixin:

    def test_200(self):
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)


class BobyViewTestCase(TestViewsMixin, TestCase):

    def setUp(self):
        mommy.make(Boby, _quantity=10, _fill_optional=True)
        self.url = reverse('home')

    def test_bobys_in_context(self):
        resp = self.client.get(self.url)
        bobys = resp.context['boby_list']
        self.assertEqual(bobys.model, Boby)


class ProfileViewTestCase(TestViewsMixin, TestCase):

    def setUp(self):
        password = '123'
        Boby.objects.create_user(username="boby", password=password)
        self.client.login(username='boby', password=password)

        self.url = reverse('profile')


class SaveOneOnOneViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('save')
        self.form_data = {'boby_pk': 1, 'buddy_pk': 3}

    @mock.patch('core.views.OneOnOneForm.is_valid')
    def test_200_in_invalid_data(self, is_valid):
        is_valid.return_value = False
        resp = self.client.post(self.url, self.form_data)
        self.assertEqual(200, resp.status_code)

    @mock.patch('core.views.SaveOneOnOneView.get_form')
    def test_200_in_valid_data(self, form):
        form.return_value.is_valid.return_value = True
        resp = self.client.post(self.url, self.form_data)
        self.assertRedirects(resp, "/")

    @mock.patch('core.views.SaveOneOnOneView.get_form')
    def test_form_save_is_called_in_valid_data(self, form):
        form.return_value.is_valid.return_value = True
        self.client.post(self.url, self.form_data)
        form.return_value.save_object.assert_called_once_with()

    @mock.patch('core.views.SaveOneOnOneView.get_form')
    def test_form_save_is_not_called_in_valid_data(self, form):
        form.return_value.is_valid.return_value = False
        self.client.post(self.url, self.form_data)
        form.return_value.save_object.assert_not_called()

