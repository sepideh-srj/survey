from django import forms
from .models import *
from django.forms.widgets import NumberInput
from PIL import Image
from django.views.generic import CreateView


class voteForm(forms.ModelForm):
    edit = forms.IntegerField(widget=NumberInput(attrs={'type':'range', 'step': '1','onchange': 'submit();'}))
    print('edit')
    class Meta:
        model = Choice
        fields = ('edit',)

class finalChoiceForm(forms.ModelForm):
    class Meta:
        model = FinalChoice
        fields = ('finalChoice',)





 


