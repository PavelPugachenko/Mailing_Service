from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class FormValidatorMixin:

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must consist of digits only")
        return phone_number


class CustomUserCreationForm(FormValidatorMixin, UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Not required field. Please enter your phone_number"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "country", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email"})
        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your country"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your phone number"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password"})


class EditProfileForm(FormValidatorMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["country", "phone_number", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].widget.attrs.update({"class": "form-control"})
        self.fields["phone_number"].widget.attrs.update({"class": "form-control"})
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
