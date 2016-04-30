from django.db import models
from django.contrib.auth.models import User


class BobyQuerySet(models.QuerySet):

    def sleeping(self, boby):
        " A Sleepy Boby who didn't meet his buddy"
        return boby.buddies.filter(
            invited__date__isnull=True,
            invited__id__isnull=False
        ).first()

    def next(self, boby):
        "The next Boby you're going to be friends with"
        sleeping = self.sleeping(boby)
        if sleeping:
            return sleeping

        buddies_ids = boby.buddies.values_list('id', flat=True)
        return self.exclude(
            id=boby.id
        ).exclude(
            id__in=buddies_ids
        ).order_by('?').first()


class BobyRelation(models.Model):
    boby_inviter = models.ForeignKey('Boby', related_name="inviter")
    boby_invited = models.ForeignKey('Boby', related_name="invited")
    date = models.DateTimeField(null=True, blank=True)


class Boby(models.Model):
    user = models.ForeignKey(User)
    buddies = models.ManyToManyField(
        'self',
        through=BobyRelation,
        through_fields=('boby_inviter', 'boby_invited'),
        symmetrical=False,
    )

    objects = BobyQuerySet.as_manager()

    def next(self):
        sleeping = self.__class__.objects.sleeping(self)
        if sleeping:
            return sleeping

        boby = self.__class__.objects.next(self)
        if boby:
            return self._add_buddy(boby)

    def _add_buddy(self, buddy):

        BobyRelation.objects.create(
            boby_inviter=self,
            boby_invited=buddy,
        )

        BobyRelation.objects.create(
            boby_inviter=buddy,
            boby_invited=self,
        )
        return buddy

    def __str__(self):
        return self.user.get_full_name() or self.user.username
