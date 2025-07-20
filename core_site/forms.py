from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(max_length=127)
    email = forms.EmailField()
    subject = forms.CharField(max_length=127)
    message = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip()
            if cleaned_data[field] == '':
                raise ValidationError(f'{field} cannot be empty.')