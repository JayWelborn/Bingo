# django Imports
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

# third party imports
from crispy_forms.layout import Submit

# app imports
from bingo.forms import CrispyBaseForm


class ContactForm(CrispyBaseForm):
    """Contact Form for sending email.

    Contact form will allow users to send email from within their browser.
    Upon form submission, the user's name, email, subject, and message will
    be assembled into an EmailMessage object for sending.

    Attributes:
        name: user's name *TODO - replace with authenticated user's name
        email: user's email address *TODO - replace with authenticated user's
            email
        subject: email's subject
        message: body of email
        cc_myself: checkbox that allows user to cc themselves

    Methods:
        __init__: add helper attributes for crispy form rendering
        send_email: combines data form form into EmailMessage object and sends.
    """

    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=50, required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    cc_myself = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Adds form helper attributes for rendering with crispy template tag.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'contact_form'
        self.helper.form_class = 'contact_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Contact Me'))

    def send_email(self):
        """
        Send email with information given via form.
        """
        if self.is_valid():

            # instantiates EmailMessage class with data from form
            contact_email = EmailMessage(
                subject=self.cleaned_data['subject'],
                to=[settings.EMAIL_HOST_USER],
                body='Sender Name: {} \nSender Email: {}\n\n {}'.format(
                    self.cleaned_data['name'],
                    self.cleaned_data['email'],
                    self.cleaned_data['message']
                )
            )

            # adds cc line if applicable
            cc_myself = self.cleaned_data['cc_myself']
            if cc_myself:
                contact_email.cc = [self.cleaned_data['email']]

            # send email
            contact_email.send()
            return contact_email

        else:
            return self.errors
