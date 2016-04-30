from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from core.models import Boby


class BobyViewTestCase(TestCase):

    def setUp(self):
        mommy.make(Boby, _quantity=10, _fill_optional=True)
        self.url = reverse('home')

    def test_200(self):
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)

    def test_bobys_in_context(self):
        resp = self.client.get(self.url)
        bobys = resp.context['boby_list']
        self.assertEqual(bobys.model, Boby)
