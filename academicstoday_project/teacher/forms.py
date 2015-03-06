from django.db import models
from django import forms

from django.forms import ModelForm, Textarea
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','body']

        labels = {

        }

        widgets = {
            'body': Textarea(attrs={'cols': 70, 'rows':10}),
        }


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['file']


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['file']
