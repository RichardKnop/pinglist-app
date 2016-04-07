from time import time

from django.shortcuts import redirect
from django.conf import settings

from apps.dashboard.forms.login import LoginForm

from . import BaseView


class LoginView(BaseView):
    form_class = LoginForm
    template_name = 'dashboard/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return self._render(
            request=request,
            form=form,
            title='Log In',
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)
        try:
            # Log in
            access_token = self.API.login(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            # Save the access token in the session
            request.session['access_token'] = access_token
            request.session['access_token_granted_at'] = time()

            # Redirect to the subscriptions page
            return redirect(settings.AFTER_LOGIN_VIEW)

        # Logging in failed, probably incorrect username and/or password
        except self.API.ErrLoginFailed as e:
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

        # Something else went wrong, timeout, network problem etc
        except Exception as e:
            form.add_error(None, str(e))
            return self._render(request=request, form=form)
