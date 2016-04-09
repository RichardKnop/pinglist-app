import logging
import uuid

from django.contrib.messages import get_messages
from django.contrib import messages
from django.conf import settings

from lib.auth import store_access_token_and_redirect
from apps.dashboard.forms.login import LoginForm
from apps import BaseView

from . import get_facebook_authorize_uri


logger = logging.getLogger(__name__)


class LoginView(BaseView):
    form_class = LoginForm
    template_name = 'dashboard/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

        # Display a potential error message
        storage = get_messages(request)
        for message in storage:
            if message.level == messages.ERROR:
                request.error = message.message
                break

        # Generate a unique state parameter and store it in the session
        state = str(uuid.uuid4())
        request.session['state'] = state

        # Store after login redirect param in the session if present in the query string
        if settings.AFTER_LOGIN_VIEW_PARAM in request.GET:
            after_login = request.GET[settings.AFTER_LOGIN_VIEW_PARAM]
            request.session[settings.AFTER_LOGIN_VIEW_PARAM] = after_login

        return self._render(
            request=request,
            form=form,
            title='Log In',
            facebook_authorize_uri=get_facebook_authorize_uri(state),
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Log in with email and password
        try:
            return store_access_token_and_redirect(
                request=request,
                access_token=self.api.login(
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                ),
            )

        # Logging in failed, probably incorrect username and/or password
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)
