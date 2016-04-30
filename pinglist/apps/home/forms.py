from django import forms

from captcha.fields import CaptchaField


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
    captcha = CaptchaField()
