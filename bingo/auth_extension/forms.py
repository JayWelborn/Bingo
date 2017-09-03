from django import forms
from django.contrib.auth.models import User

from crispy_forms.layout import Submit

from bingo.forms import CrispyBaseForm

from .models import UserProfile


class RegistrationForm(CrispyBaseForm):
    """Form for registering new users. Only contains fields required
    for user objects. Redirect will take users to page where they can
    edit their profiles.

    Fields:
        username: User's name. Will be slugified for URL upon form save
        email: User's email address
        password: Password. Hashed before storing in the database.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """

    # specify widget for password input
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'registration_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def save(self):
        """
        Here we override the parent class's 'save' method to create a
        UserProfile instance matching the User in the form.
        """
        if self.is_valid():
            user = User.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
            )

            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']

            if password and password == password_confirmation:
                user.set_password(self.cleaned_data['password'])
                user.save()

            else:
                raise forms.ValidationError('Passwords Entered Do Not Match')

            profile = UserProfile.objects.create(user=user)
            profile.save()
            return user

        else:
            return self.errors
