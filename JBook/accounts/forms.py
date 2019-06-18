from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
class UserCreateForm(UserCreationForm):

    class Meta():
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        model = get_user_model()

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.fields['email'].label = 'Email Address'

class UserForm(forms.ModelForm):
    class Meta():
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['first_name'].required = True
        # self.helper = FormHelper(self)
        # self.helper.form_tag = False
        # self.helper.layout = Layout('first_name', 'last_name')


class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = ['about', 'avatar', 'location', 'avatar', 'birth_date', 'branch']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False
        self.fields['avatar'].label = 'Profile Picture'
