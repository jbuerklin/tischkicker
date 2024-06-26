from django.forms import ModelForm, CharField, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from braschüne.models import Profile, User


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'hx-post': '/accounts/profile/', 'hx-target': '#profile-form', 'hx-disabled-elt': 'find input[type=submit]'}
        self.helper.add_input(Submit('submit-profile', 'Submit'))

    class Meta:
        model = Profile
        fields = ['image', 'sicherungskasten']


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'hx-swap': 'outerHTML', 'hx-post': '/accounts/profile/', 'hx-disabled-elt': 'find input[type=submit]'}
        self.helper.add_input(Submit('submit-user', 'Submit'))

    class Meta:
        model = User
        fields = ['username', 'password']