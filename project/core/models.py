from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from django.core.exceptions import PermissionDenied


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

        return self.candidates(boby).order_by('?').first()

    def candidates(self, boby):
        buddies_ids = boby.buddies.values_list('id', flat=True)
        return self.exclude(
            id=boby.id
        ).exclude(
            id__in=buddies_ids
        )


class BobyManager(UserManager):

    def get_queryset(self):
        return BobyQuerySet(self.model, using=self._db)

    def __getattr__(self, attr):
        return getattr(self.get_queryset(), attr)


class BobyRelationManager(models.Manager):

    def update_relation(self, boby, boby_pk, buddy_pk):

        relation = self.model.objects.get(
            inviter=boby_pk,
            invited=buddy_pk,
        )

        if not boby.has_perm('core.change_bobyrelation', relation):
            raise PermissionDenied

        relation = self.get_queryset().get(
            inviter_id=boby_pk,
            invited_id=buddy_pk,
        )
        r_relation = self.get_queryset().get(
            invited_id=boby_pk,
            inviter_id=buddy_pk,
        )
        relation.date = timezone.now()
        r_relation.date = timezone.now()
        relation.save()
        r_relation.save()


class BobyRelation(models.Model):
    inviter = models.ForeignKey('Boby', related_name="inviter")
    invited = models.ForeignKey('Boby', related_name="invited")
    date = models.DateTimeField(null=True, blank=True)

    objects = BobyRelationManager()


class Boby(AbstractUser):
    buddies = models.ManyToManyField(
        'self',
        through=BobyRelation,
        through_fields=('inviter', 'invited'),
        symmetrical=False,
    )

    objects = BobyManager()

    def next(self):
        sleeping = self.__class__.objects.sleeping(self)
        if sleeping:
            return sleeping

        boby = self.__class__.objects.next(self)
        if boby:
            return self.add_buddy(boby)

    def candidates(self):
        return self.__class__.objects.candidates(self)

    def add_buddy(self, buddy):

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

    class Meta:
        ordering = ('email',)
