from django import forms
from .models import Kick


MAX_KICK_LENGTH = 240


class KickForm(forms.ModelForm):
    class Meta:
        model = Kick
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_KICK_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content
