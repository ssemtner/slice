from django import forms


class UploadClipForm(forms.Form):
    title = forms.CharField(max_length=100)
    video = forms.FileField()
