from django.test import TestCase
from core.models import Boby, BobyRelation
from model_mommy import mommy


class BobyModelTestCase(TestCase):

    def test_boby_is_created(self):
        mommy.make(Boby, id=42)
        bobby = Boby.objects.get(id=42)
        self.assertEquals(42, bobby.id)

    def test_boby_has_friends(self):
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby._add_buddy(boby_buddy)
        self.assertEquals(boby_buddy, boby.buddies.first())

    def test_if_boby_friends_are_frieds_with_boby(self):
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby._add_buddy(boby_buddy)
        self.assertEquals(boby_buddy, boby.buddies.first())

    def test_sleeping_boby(self):
        "Sleeping boby is a boby who forgot to meet"
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby._add_buddy(boby_buddy)
        sleeping = Boby.objects.sleeping(boby)
        self.assertEquals(boby_buddy, sleeping)

    def test_next_boby_is_last_without_a_date(self):
        "Sleeping boby is a boby who forgot to meet"
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        next = boby.next()
        mommy.make(Boby, id=50)
        self.assertEquals(boby_buddy, next)

    def test_get_next_boby_gets_sleeping_boby(self):
        boby = mommy.make(Boby, id=42, _fill_optional=True)
        boby_buddy = mommy.make(Boby, id=23, _fill_optional=True)
        mommy.make(BobyRelation, boby_inviter=boby, boby_invited=boby_buddy)
        mommy.make(BobyRelation, _fill_optional=True, _quantity=5)
        next = boby.next()
        self.assertEquals(boby_buddy, next)
