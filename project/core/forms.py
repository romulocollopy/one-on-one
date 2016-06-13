from django import forms
from django.core.exceptions import PermissionDenied
import rules
from .models import BobyRelation, Boby


class OneOnOneForm(forms.Form):
    boby_pk = forms.IntegerField()
    buddy_pk = forms.IntegerField()
    create_relation = forms.NullBooleanField()

    def is_valid(self, boby, *args, **kwargs):
        self.boby = boby
        return super().is_valid(*args, **kwargs)

    def save_object(self):
        if self.cleaned_data.get('create_relation') is True:
            self._create_relation()
        BobyRelation.objects.update_relation(self.boby, **self.cleaned_data)

    def _create_relation(self):
        BobyRelation.objects.create(inviter_id=self.cleaned_data['boby_pk'],
                                    invited_id=self.cleaned_data['buddy_pk'])

        BobyRelation.objects.create(invited_id=self.cleaned_data['boby_pk'],
                                    inviter_id=self.cleaned_data['buddy_pk'])


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
