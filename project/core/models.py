from django.db import models
from django.contrib.auth.models import AbstractUser


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
    inviter = models.ForeignKey('Boby', related_name="inviter")
    invited = models.ForeignKey('Boby', related_name="invited")
    date = models.DateTimeField(null=True, blank=True)


class Boby(AbstractUser):
    buddies = models.ManyToManyField(
        'self',
        through=BobyRelation,
        through_fields=('inviter', 'invited'),
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
            inviter=self,
            invited=buddy,
        )

        BobyRelation.objects.create(
            inviter=buddy,
            invited=self,
        )
        return buddy

    def __str__(self):
        return self.get_full_name() or self.username
