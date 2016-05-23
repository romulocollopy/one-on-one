from django import forms
from django.core.exceptions import PermissionDenied
from .models import BobyRelation


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
