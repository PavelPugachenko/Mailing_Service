from django import forms

from .models import MailingUnit, MailReceiver, Message


class MailingUnitForm(forms.ModelForm):
    receivers = forms.ModelMultipleChoiceField(
        queryset=MailReceiver.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check"}),
        label="Mail Receivers",
    )

    class Meta:
        model = MailingUnit
        fields = ["message", "receivers"]

    def __init__(self, *args, **kwargs):
        super(MailingUnitForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-control"})


class MailReceiverForm(forms.ModelForm):
    class Meta:
        model = MailReceiver
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MailReceiverForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter email"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Enter full name"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Enter comment"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "Enter message title"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Enter message body"})
