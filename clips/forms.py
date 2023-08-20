from django import forms
from .models import Clip


class UploadClipForm(forms.Form):
    video = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "bg-zinc-200 rounded-lg p-2",
                "@change": "loadPreview",
            }
        ),
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "bg-zinc-200 rounded-lg p-2"}),
    )
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "bg-zinc-200 rounded-lg p-2"}),
    )
    visibility = forms.ChoiceField(
        choices=Clip.VisibilityType.choices,
        widget=forms.Select(attrs={"class": "bg-zinc-200 rounded-lg p-2"}),
        initial=Clip.VisibilityType.HIDDEN,
    )
