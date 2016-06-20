import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseServerError

from lib.auth import logged_in
from apps import BaseView
from apps.settings.forms import (
    SettingsForm,
    ChangePasswordForm,
)


logger = logging.getLogger('django')


class IndexView(BaseView):
    form_class = SettingsForm
    template_name = 'settings/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_me(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching user failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class(initial={
            'first_name': str(user['first_name']),
            'last_name': str(user['last_name']),
            'slack_incoming_webhook': str(user['slack_incoming_webhook']),
            'slack_channel': str(user['slack_channel']),
        })

        return self._render(
            request=request,
            form=form,
            user=user,
        )

    @logged_in
    def post(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_me(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching user failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                user=user,
            )

        # Update the user profile
        try:
            user['first_name'] = form.cleaned_data['first_name']
            user['last_name'] = form.cleaned_data['last_name']
            user['slack_incoming_webhook'] = form.cleaned_data['slack_incoming_webhook']
            user['slack_channel'] = form.cleaned_data['slack_channel']
            self.api.update_user(
                access_token=request.session['access_token']['access_token'],
                user=user,
            )

            # Push success message and redirect
            messages.success(request, 'Settings updated successfully')
            return redirect('settings:index')

        # Updating user failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                user=user,
            )

    def _render(self, request, form, user):
        return super(IndexView, self)._render(
            request=request,
            form=form,
            user=user,
            title='Settings - Pinglist',
            active_link='settings',
        )


class ChangePasswordView(BaseView):
    form_class = ChangePasswordForm
    template_name = 'settings/change-password.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_me(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching user failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class()

        return self._render(
            request=request,
            form=form,
            user=user,
        )

    @logged_in
    def post(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_me(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching user failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                user=user,
            )

        if form.cleaned_data['new_password'] != form.cleaned_data['new_password_again']:
            form.add_error(None, 'Both new passwords must match')
            return self._render(
                request=request,
                form=form,
                user=user,
            )

        # Change the password
        try:
            user['password'] = form.cleaned_data['old_password']
            user['new_password'] = form.cleaned_data['new_password']
            self.api.update_user(
                access_token=request.session['access_token']['access_token'],
                user=user,
            )

            # Push success message and redirect
            messages.success(request, 'Password changed successfully')
            return redirect('settings:change_password')

        # Changing password failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                user=user,
            )

    def _render(self, request, form, user):
        return super(ChangePasswordView, self)._render(
            request=request,
            form=form,
            user=user,
            title='Change Password - Pinglist',
            active_link='change_password',
        )
