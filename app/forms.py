from django import forms

from app.models import Link


class CommitForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url','title', 'cover', 'size','desc', 'contact']