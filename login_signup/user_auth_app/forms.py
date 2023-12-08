from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email',
                  'password1', 'password2', 'address_line1', 'city', 'state', 'pincode', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
