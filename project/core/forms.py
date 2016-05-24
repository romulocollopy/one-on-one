from django import forms
from django.core.exceptions import PermissionDenied
import rules
from .models import BobyRelation, Boby


class OneOnOneForm(forms.Form):
    boby_pk = forms.IntegerField()
    buddy_pk = forms.IntegerField()

    def is_valid(self, boby, *args, **kwargs):
        valid = super().is_valid(*args, **kwargs)
        if not valid:
            return False

        relation = BobyRelation.objects.get(
            inviter=self.cleaned_data['boby_pk'],
            invited=self.cleaned_data['buddy_pk']
        )

        if boby.has_perm('core.change_bobyrelation', relation):
            self.boby = boby
            return True

        raise PermissionDenied

    def save_object(self):
        BobyRelation.objects.update_relation(self.boby, **self.cleaned_data)


class UploadUsersForm(forms.Form):

    file = forms.FileField()

    def is_valid(self, boby):
        valid = super(UploadUsersForm, self).is_valid()
        if not valid:
            return False
        if not rules.test_rule('can_upload_users', boby):
            raise PermissionDenied
        return True

    def save(self):
        csvfile = self.files['file']
        lines = [row.split(",") for row in
                 csvfile.read().decode().split('\n')[1:]][:-1]
        bobylist = [
            Boby(
                first_name=row[0].replace('"', ''),
                last_name=row[1].replace('"', ''),
                email=row[2].replace('"', ''),
                username=row[2].replace('"', '').split('@')[0],
            ) for row in lines
        ]
        Boby.objects.bulk_create(bobylist)
