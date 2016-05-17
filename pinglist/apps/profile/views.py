import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseServerError

from lib.auth import logged_in
from apps import BaseView
from apps.profile.forms import (
    ProfileForm,
    ChangePasswordForm,
)


logger = logging.getLogger('django')


class IndexView(BaseView):
    form_class = ProfileForm
    template_name = 'profile/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_user(
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
            user = self.api.get_user(
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

        # Update the user
        try:
            user['first_name'] = form.cleaned_data['first_name']
            user['last_name'] = form.cleaned_data['last_name']
            self.api.update_user(
                access_token=request.session['access_token']['access_token'],
                user=user,
            )

            # Push success message and redirect
            messages.success(request, 'Profile updated successfully')
            return redirect('profile:index')

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
            title='Profile - Pinglist',
            active_link='profile',
        )


class ChangePasswordView(BaseView):
    form_class = ChangePasswordForm
    template_name = 'profile/change-password.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the user
        try:
            user = self.api.get_user(
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
            user = self.api.get_user(
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
            return redirect('profile:change_password')

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
