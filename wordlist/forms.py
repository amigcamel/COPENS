#-*-coding:utf-8-*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from cwm.forms import DB_CHOICE

class WordlistForm(forms.Form):
    database = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                         choices=DB_CHOICE, 
                                         error_messages={'required':"請至少選一項"},
                                        ) 
    stopwords = forms.BooleanField(required=False)
    stopword_level = forms.IntegerField(widget=forms.HiddenInput(), initial=100, required=False)
    punctuations = forms.BooleanField(required=False)
    topnword = forms.IntegerField(widget=forms.HiddenInput(), initial=20)
    
