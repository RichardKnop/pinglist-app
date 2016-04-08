import logging

from django.contrib.messages import get_messages
from django.contrib import messages

from apps.dashboard.forms.login import LoginForm
from apps.api import store_access_token_and_redirect

from . import BaseView, get_facebook_authorize_uri


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
                form.clean()
                form.add_error(None, message.message)
                break
            logger.info(message.message)

        return self._render(
            request=request,
            form=form,
            title='Log In',
            facebook_authorize_uri=get_facebook_authorize_uri(),
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Log in with email and password
        try:
            return store_access_token_and_redirect(
                request=request,
                access_token=self.API.login(
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                ),
            )

        # Logging in failed, probably incorrect username and/or password
        except self.API.ErrLoginFailed as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

        # Something else went wrong, timeout, network problem etc
        except Exception as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)
