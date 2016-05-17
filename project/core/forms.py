from django import forms
from .models import BobyRelation


class OneOnOneForm(forms.Form):
    boby_pk = forms.IntegerField()
    buddy_pk = forms.IntegerField()

    def save_object(self):
        BobyRelation.objects.update_relation(**self.cleaned_data)
