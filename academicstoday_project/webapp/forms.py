from django.db import models
from django import forms

from django.forms import ModelForm
from webapp.models import EssaySubmission

class EssaySubmissionForm(forms.ModelForm):
    class Meta:
        model = EssaySubmission

    # Function will apply validation on the 'file' upload column in the table.
    def clean_file(self):
        upload = self.cleaned_data['file']
        content_type = upload.content_type
        if content_type in ['application/pdf']:
            if upload._size <= 20971520:
                return upload
            else:
                raise forms.ValidationError("Cannot exceed 20MB size")
        else:
            raise forms.ValidationError("Only accepting PDF files for essays.")