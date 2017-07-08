from django import forms
from django.forms import ModelForm, PasswordInput
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from mooi.models import Profile

class LoginForm(ModelForm):
    """Manages logins using email and password. Some code borrowed from django.contrib.auth.forms."""
    
    password = forms.CharField(max_length=128, widget=PasswordInput(render_value=False))
    
    class Meta:
        model = User
        fields = ('email',)
        
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        
        super(LoginForm, self).clean()
        
        username = self.cleaned_data.get('email', False)
        password = self.cleaned_data.get('password', False)

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct email and password. Note that the password is case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
        
class SavePasswordsForm(forms.Form):
    """Form used to set a password for an account."""
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    passwordConfirmation = forms.CharField(label="Re-type Password", widget=forms.PasswordInput)
    
    def clean(self):
        if 'password' in self.cleaned_data and 'passwordConfirmation' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['passwordConfirmation']:
                raise forms.ValidationError('You must type the same password each time')
        return self.cleaned_data

        
class RegisterForm(SavePasswordsForm):
    """Registration form."""
    email = forms.EmailField(label="Email")
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'password', 'passwordConfirmation']


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile