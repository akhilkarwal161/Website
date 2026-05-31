from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    # Honeypot field - must be left blank by humans
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none;', 'autocomplete': 'off', 'tabindex': '-1'}),
        label=''
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        if honeypot:
            # Raise a ValidationError to mark the form invalid if a bot filled the honeypot
            raise forms.ValidationError("Spam detected.")
        return cleaned_data
