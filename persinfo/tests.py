from django.test import TestCase
from persinfo.forms import ContactForm

class ContactFormSpamTestCase(TestCase):
    def test_valid_submission_allowed(self):
        """Test that a standard, clean, English contact submission is valid."""
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Inquiry about Django Development',
            'message': 'Hello, I would love to talk about building a website. Thank you!'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cyrillic_spam_rejected(self):
        """Test that Cyrillic text (common Russian spam) is detected and rejected."""
        # Cyrillic in name
        form = ContactForm(data={
            'name': 'Иван',
            'email': 'bot@yandex.ru',
            'subject': 'Important',
            'message': 'This is a test message.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Spam detected.', form.errors.get('__all__', []))

        # Cyrillic in subject
        form = ContactForm(data={
            'name': 'Spam Bot',
            'email': 'bot@yandex.ru',
            'subject': 'быстрый исправление',
            'message': 'This is a test message.'
        })
        self.assertFalse(form.is_valid())

        # Cyrillic in message
        form = ContactForm(data={
            'name': 'Spam Bot',
            'email': 'bot@yandex.ru',
            'subject': 'Important',
            'message': 'Срочный ремонтные работы машин-автоматов'
        })
        self.assertFalse(form.is_valid())

    def test_html_links_in_message_rejected(self):
        """Test that HTML anchor tags or href links in the message trigger spam detection."""
        form = ContactForm(data={
            'name': 'rembytexBX',
            'email': 'remontbytex@yandex.ru',
            'subject': 'быстрый исправление стирального оборудования',
            'message': 'Hello, look at <a href="http://spam-link.com">Click Here</a>'
        })
        self.assertFalse(form.is_valid())

    def test_url_in_name_rejected(self):
        """Test that websites/URLs in the name field are blocked as spam."""
        form = ContactForm(data={
            'name': 'http://spam-name.ru',
            'email': 'spammer@yandex.ru',
            'subject': 'Hello',
            'message': 'This is a standard message without links.'
        })
        self.assertFalse(form.is_valid())

