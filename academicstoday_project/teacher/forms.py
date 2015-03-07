from django.db import models
from django import forms
from django.forms.extras.widgets import Select, SelectDateWidget
from django.conf import settings

from django.forms import ModelForm, Textarea
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy
from registrar.models import Lecture
from registrar.models import Assignment

# Django Widgets
# https://docs.djangoproject.com/en/1.7/ref/forms/widgets/

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


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['lecture_id', 'lecture_num', 'week_num', 'title', 'description', 'youtube_url', 'vimeo_url', 'preferred_service']

ASSIGNMENT_TYPE_CHOICES = ((settings.ESSAY_ASSIGNMENT_TYPE, 'Essay'),
                           (settings.MULTIPLECHOICE_ASSIGNMENT_TYPE, 'Multiple-Choice'),
                           (settings.TRUEFALSE_ASSIGNMENT_TYPE, 'True/False'),
                           (settings.RESPONSE_ASSIGNMENT_TYPE, 'Response'))

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'assignment_num', 'title', 'description', 'type', 'due_date']

        widgets = {
            'due_date': SelectDateWidget(),
            'type': Select(choices=ASSIGNMENT_TYPE_CHOICES),
        }