from django import forms
from .models import Subject, Choice

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_text']  # Fields you want to include in the form

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']  # Fields you want to include in the form
