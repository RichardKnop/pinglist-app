import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseServerError

from lib.auth import logged_in
from apps import BaseView
from apps.profile.forms import ProfileForm


logger = logging.getLogger(__name__)


class IndexView(BaseView):
    form_class = ProfileForm
    template_name = 'profile/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the profile
        try:
            profile = self.api.get_profile(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching profile failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Init the form
        form = self.form_class(initial={
            'first_name': str(profile['first_name']),
            'last_name': str(profile['last_name']),
        })

        return self._render(
            request=request,
            form=form,
            profile=profile,
        )

    @logged_in
    def post(self, request, *args, **kwargs):
        # Fetch the profile
        try:
            profile = self.api.get_profile(
                access_token=request.session['access_token']['access_token'],
            )

        # Fetching profile failed
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
                profile=profile,
            )

        # Update the profile
        try:
            profile['first_name'] = form.cleaned_data['first_name']
            profile['last_name'] = form.cleaned_data['last_name']
            self.api.update_profile(
                access_token=request.session['access_token']['access_token'],
                profile=profile,
            )

            # Push success message and redirect back to index view
            messages.success(request, 'Profile updated successfully')
            return redirect('profile:index')

        # Updating profile failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                profile=profile,
            )

    def _render(self, request, form, profile):
        return super(IndexView, self)._render(
            request=request,
            form=form,
            profile=profile,
            title='Profile',
            active_link='profile',
        )