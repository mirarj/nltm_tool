from django import forms

class UploadDFDFileForm(forms.Form):
    inputFile = forms.FileField()