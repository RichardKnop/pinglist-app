import logging

from django.shortcuts import redirect

from apps import BaseView
from apps.web.forms import (
    ConfirmInvitationForm,
    ConfirmPasswordResetForm,
)

logger = logging.getLogger('django')


class ConfirmEmailView(BaseView):
    template_name = 'web/confirm-email.html'

    def get(self, request, reference, *args, **kwargs):
        # Confirm the email
        self.api.confirm_email(reference=reference)

        # Unhandled exception will go to 500.html

        return super(ConfirmEmailView, self)._render(
            request=request,
            title='Email Confirmation - Pinglist',
        )


class ConfirmInvitationView(BaseView):
    form_class = ConfirmInvitationForm
    template_name = 'web/confirm-invitation.html'

    def get(self, request, reference, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(
            request=request,
            form=form,
            reference=reference,
        )

    def post(self, request, reference, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                reference=reference,
            )

        if form.cleaned_data['password'] != form.cleaned_data['password_again']:
            form.add_error(None, "Passwords must match")
            return self._render(
                request=request,
                form=form,
                reference=reference,
            )

        # Confirm the invitation
        self.api.confirm_invitation(
            reference=reference,
            password=form.cleaned_data['password'],
        )

        # Unhandled exception will go to 500.html

        # Redirect to success page
        return redirect('web:confirm_invitation_success')

    def _render(self, request, form, reference):
        return super(ConfirmInvitationView, self)._render(
            request=request,
            form=form,
            reference=reference,
            title='Set Password - Pinglist',
        )


class ConfirmInvitationSuccessView(BaseView):
    template_name = 'web/confirm-invitation-success.html'

    def get(self, request, *args, **kwargs):
        return super(ConfirmInvitationSuccessView, self)._render(
            request=request,
            title='Invitation Confirmed - Pinglist',
        )


class ConfirmPasswordResetView(BaseView):
    form_class = ConfirmPasswordResetForm
    template_name = 'web/confirm-password-reset.html'

    def get(self, request, reference, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(
            request=request,
            form=form,
            reference=reference,
        )

    def post(self, request, reference, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                reference=reference,
            )

        if form.cleaned_data['password'] != form.cleaned_data['password_again']:
            form.add_error(None, "Passwords must match")
            return self._render(
                request=request,
                form=form,
                reference=reference,
            )

        # Confirm the password reset
        self.api.confirm_password_reset(
            reference=reference,
            password=form.cleaned_data['password'],
        )

        # Unhandled exception will go to 500.html

        # Redirect to success page
        return redirect('web:confirm_password_reset_success')

    def _render(self, request, form, reference):
        return super(ConfirmPasswordResetView, self)._render(
            request=request,
            form=form,
            reference=reference,
            title='Set New Password - Pinglist',
        )


class ConfirmPasswordResetSuccessView(BaseView):
    template_name = 'web/confirm-password-reset-success.html'

    def get(self, request, *args, **kwargs):
        return super(ConfirmPasswordResetSuccessView, self)._render(
            request=request,
            title='Password Reset Confirmed - Pinglist',
        )

