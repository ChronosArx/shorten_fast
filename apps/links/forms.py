from django.forms import ModelForm
from django import forms
from .models import Link


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ["original_url"]
        widgets = {
            "original_url": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Ingresa tu url.",
                }
            )
        }
