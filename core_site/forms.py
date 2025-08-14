from django import forms
from django.core.exceptions import ValidationError
from .utils import send_email

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
        subject = '[Portfolio Inqury] {subject}'.format(subject=cleaned_data.get('subject'))
        body = 'Name: {name}\nEmail: {email}\n\nMESSAGE:\n{message}'.format(name=cleaned_data.get('name'), email=cleaned_data.get('email'), message=cleaned_data.get('message'))
        reply_to = (cleaned_data.get('email'),)
        email_success = None
        try:
            result = send_email(subject, body, reply_to=reply_to)
            email_success = bool(result)
        except Exception:
            email_success = False
        cleaned_data['email_success'] = email_success