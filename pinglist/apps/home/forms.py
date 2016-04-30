from django import forms


class ContactForm(forms.Form):

    name = forms.CharField(
        required=True,
        label='Your Name',
    )
    email = forms.EmailField(
        required=True,
        label='Your Email',
    )
    subject = forms.CharField(
        required=True,
        label='Subject',
    )
    message = forms.CharField(
        required=True,
        label='Message',
    )
