#-*-coding:utf-8-*-
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required':'required'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'required':'required'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'required':'required'}))

