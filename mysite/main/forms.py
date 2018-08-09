from django import forms

class IndexForm(forms.Form):
    link = forms.CharField()