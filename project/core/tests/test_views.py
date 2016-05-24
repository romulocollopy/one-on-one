import mock

from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from project.core.models import Boby


class TestViewGetMixin:

    def test_200(self):
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)


class LoginMixin:
    def login(self):
        password = '123'
        self.boby = Boby.objects.create_user(username="boby",
                                             password=password)
        self.client.login(username='boby', password=password)


class BobyViewTestCase(TestViewGetMixin, TestCase):

    def setUp(self):
        mommy.make(Boby, _quantity=10, _fill_optional=True)
        self.url = reverse('home')

    def test_bobys_in_context(self):
        resp = self.client.get(self.url)
        bobys = resp.context['boby_list']
        self.assertEqual(bobys.model, Boby)


class ProfileViewTestCase(LoginMixin, TestViewGetMixin, TestCase):

    def setUp(self):
        self.login()
        self.url = reverse('profile')


class SaveOneOnOneViewTestCase(LoginMixin, TestCase):

    def setUp(self):
        self.login()
        self.url = reverse('save')
        self.form_data = {'boby_pk': 1, 'buddy_pk': 3}

    @mock.patch('project.core.views.OneOnOneForm.is_valid')
    def test_200_in_invalid_data(self, is_valid):
        is_valid.return_value = False
        resp = self.client.post(self.url, self.form_data)
        self.assertEqual(200, resp.status_code)

    @mock.patch('project.core.views.SaveOneOnOneView.get_form')
    def test_200_in_valid_data(self, form):
        form.return_value.is_valid.return_value = True
        resp = self.client.post(self.url, self.form_data)
        self.assertRedirects(resp, "/")

    @mock.patch('project.core.views.SaveOneOnOneView.get_form')
    def test_form_save_is_called_in_valid_data(self, form):
        form.return_value.is_valid.return_value = True
        self.client.post(self.url, self.form_data)
        form.return_value.save_object.assert_called_once_with()

    @mock.patch('project.core.views.SaveOneOnOneView.get_form')
    def test_form_save_is_not_called_in_valid_data(self, form):
        form.return_value.is_valid.return_value = False
        self.client.post(self.url, self.form_data)
        form.return_value.save_object.assert_not_called()


class UploadBobyViewTestCase(LoginMixin, TestViewGetMixin, TestCase):

    def setUp(self):
        self.login()
        self.url = reverse('upload_users')

    @mock.patch('project.core.views.UploadUsersView.get_form')
    def test_redirects_in_form_valid(self, mock_form):
        mock_form.return_value.is_valid.return_value = True
        resp = self.client.post(self.url)
        self.assertRedirects(resp, reverse('home'))

    @mock.patch('project.core.views.UploadUsersView.get_form')
    def test_calls_save_in_form_valid(self, mock_form):
        mock_form.return_value.is_valid.return_value = True
        self.client.post(self.url)
        mock_form.return_value.save.assert_called_once_with()

    @mock.patch('project.core.views.UploadUsersView.get_form')
    def test_stays_on_page_in_form_invalid(self, mock_form):
        mock_form.return_value.is_valid.return_value = False
        resp = self.client.post(self.url)
        self.assertEqual(200, resp.status_code)


class CandidatesViewTestCase(LoginMixin, TestViewGetMixin, TestCase):

    def setUp(self):
        self.login()
        self.url = reverse('candidates')

    @mock.patch('project.core.views.Boby.objects.candidates')
    def test_candidates_is_called(self, mock_candidates):
        self.client.get(self.url)
        mock_candidates.assert_called_once_with(self.boby)
