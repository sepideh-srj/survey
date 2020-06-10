from django import forms
from .models import *
from django.forms.widgets import NumberInput
from django.views.generic import CreateView


class voteForm(forms.ModelForm):
    class Meta:

        model = Choice
        fields = ['flash', 'ambient', 'flashTemp','ambientBrightness']




 


