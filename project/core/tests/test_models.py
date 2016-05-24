from django.test import TestCase
from project.core.models import Boby, BobyRelation
from model_mommy import mommy


class BobyModelTestCase(TestCase):

    def test_boby_is_created(self):
        mommy.make(Boby, id=42)
        bobby = Boby.objects.get(id=42)
        self.assertEquals(42, bobby.id)

    def test_boby_has_friends(self):
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby.add_buddy(boby_buddy)
        self.assertEquals(boby_buddy, boby.buddies.first())

    def test_if_boby_friends_are_frieds_with_boby(self):
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby.add_buddy(boby_buddy)
        self.assertEquals(boby_buddy, boby.buddies.first())

    def test_sleeping_boby(self):
        "Sleeping boby is a boby who forgot to meet"
        boby = mommy.make(Boby, id=42)
        boby_buddy = mommy.make(Boby, id=23)
        boby.add_buddy(boby_buddy)
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
        mommy.make(BobyRelation, inviter=boby, invited=boby_buddy)
        mommy.make(BobyRelation, _fill_optional=True, _quantity=5)
        next = boby.next()
        self.assertEquals(boby_buddy, next)

    def test_get_candidates_queryset(self):
        boby = mommy.make(Boby, id=42, _fill_optional=True)
        boby_buddy = mommy.make(Boby, id=23, _fill_optional=True)
        mommy.make(BobyRelation, inviter=boby, invited=boby_buddy)
        mommy.make(BobyRelation, _fill_optional=True, _quantity=5)
        candidates = list(boby.candidates())
        self.assertNotIn(boby_buddy, candidates)


class BobyRelationTestCase(TestCase):

    def setUp(self):
        self.boby = mommy.make(Boby, id=42)
        self.boby_buddy = mommy.make(Boby, id=23)
        mommy.make(BobyRelation, inviter=self.boby, invited=self.boby_buddy)
        mommy.make(BobyRelation, inviter=self.boby_buddy, invited=self.boby)

    def test_update_relation(self):
        BobyRelation.objects.update_relation(self.boby, self.boby.id,
                                             self.boby_buddy.id)

        br1 = BobyRelation.objects.get(
            inviter=self.boby.id,
            invited=self.boby_buddy.id,
        )
        br2 = BobyRelation.objects.get(
            inviter=self.boby_buddy.id,
            invited=self.boby.id,
        )

        self.assertIsNotNone(br1.date)
        self.assertIsNotNone(br2.date)
