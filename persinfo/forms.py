import re
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    # Honeypot field - must be left blank by humans
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none;', 'autocomplete': 'off', 'tabindex': '-1'}),
        label=''
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def clean(self):
        cleaned_data = super().clean()
        website = cleaned_data.get('website')
        if website:
            # Raise a ValidationError to mark the form invalid if a bot filled the honeypot
            raise forms.ValidationError("Spam detected.")

        name = cleaned_data.get('name', '')
        subject = cleaned_data.get('subject', '')
        message = cleaned_data.get('message', '')

        # 1. Cyrillic character detection (blocks Russian bot spam completely)
        cyrillic_pattern = re.compile(r'[\u0400-\u04FF]')
        if (cyrillic_pattern.search(name) or 
            cyrillic_pattern.search(subject) or 
            cyrillic_pattern.search(message)):
            raise forms.ValidationError("Spam detected.")

        # 2. Block HTML/BBCode link formatting (common spam indicators)
        html_link_pattern = re.compile(r'<a\s|href=|\[url\]|\[url=|http://|https://', re.IGNORECASE)
        
        # Real people don't put URLs in their name or subject
        if html_link_pattern.search(name) or html_link_pattern.search(subject):
            raise forms.ValidationError("Spam detected.")

        # Real message shouldn't contain HTML anchor tags/BBCode spam links
        if '<a ' in message.lower() or 'href=' in message.lower() or '[url=' in message.lower():
            raise forms.ValidationError("Spam detected.")

        # 3. Block messages with common spam keywords
        spam_keywords = [
            'betting', 'casino', 'bookmaker', '1xbet', 'crypto', 'seo', 'traffic', 
            'porn', 'sex', 'dating', 'jackpot', 'viagra', 'cialis', 'invest', 'gambling',
            'btc', 'withdraw', 'girls', 'is.gd', 'yt.vu', 'bit.ly', 't.me', 'binance', 'usdt',
            'investment'
        ]
        message_lower = message.lower()
        subject_lower = subject.lower()
        if any(keyword in message_lower for keyword in spam_keywords) or \
           any(keyword in subject_lower for keyword in spam_keywords):
            raise forms.ValidationError("Spam detected.")

        # 4. Block messages with multiple URLs
        url_count = message_lower.count('http://') + message_lower.count('https://')
        if url_count > 1:
            raise forms.ValidationError("Spam detected.")

        # 5. Block specific email domains or TLDs common in spam
        email = cleaned_data.get('email', '').lower()
        spam_email_tlds = ['.ru', '.su', '.cn', '.top', '.xyz', '.info']
        if any(email.endswith(tld) for tld in spam_email_tlds):
            raise forms.ValidationError("Spam detected.")

        return cleaned_data

