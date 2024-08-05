from django.forms import forms

class FileForm(forms.Form):
    file = forms.FileField()