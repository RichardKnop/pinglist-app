import logging
import uuid
import requests

from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect

from lib.auth import store_access_token_and_redirect
from apps import BaseView
from apps.auth.forms import (
    RegisterForm,
    LoginForm,
    ResetPasswordForm,
)

from . import (
    get_facebook_authorize_uri,
    get_facebook_redirect_uri
)

logger = logging.getLogger('django')


class RegisterView(BaseView):
    form_class = RegisterForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Register with email and password
        try:
            self.api.register(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            # Push success message and redirect to the login view
            messages.success(request, 'Thank you for registering. You can now log in to your account.')
            return redirect('auth:login')

        # Registering failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        # Generate a unique state parameter and store it in the session
        state = str(uuid.uuid4())
        request.session['state'] = state

        return super(RegisterView, self)._render(
            request=request,
            form=form,
            title='Register',
            facebook_authorize_uri=get_facebook_authorize_uri(state),
            active_link='register',
        )


class LoginView(BaseView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
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
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        # Generate a unique state parameter and store it in the session
        state = str(uuid.uuid4())
        request.session['state'] = state

        # Store after login redirect param in the session if present in the query string
        if settings.AFTER_LOGIN_VIEW_PARAM in request.GET:
            after_login = request.GET[settings.AFTER_LOGIN_VIEW_PARAM]
            request.session[settings.AFTER_LOGIN_VIEW_PARAM] = after_login

        return super(LoginView, self)._render(
            request=request,
            form=form,
            title='Log In',
            facebook_authorize_uri=get_facebook_authorize_uri(state),
            active_link='login',
        )


class FacebookRedirectView(BaseView):
    def get(self, request, *args, **kwargs):
        # Facebook redirected with an error
        if 'error' in request.GET:
            messages.error(request, request.GET.get('error_description'))
            return redirect(settings.LOGIN_VIEW)

        # Verify the state is the same as what we stored in the session previously
        if request.GET.get('state', '') != request.session.get('state', ''):
            messages.error(request, 'State mismatch')
            return redirect(settings.LOGIN_VIEW)

        # Exchange Facebook authorization code for an access token
        try:
            r = requests.get(
                url='https://graph.facebook.com/v2.3/oauth/access_token',
                params={
                    'client_id': settings.FACEBOOK_APP_ID,
                    'redirect_uri': get_facebook_redirect_uri(),
                    'client_secret': settings.FACEBOOK_APP_SECRET,
                    'code': request.GET.get('code', ''),
                },
                allow_redirects=False,
            )
            logger.debug(r)
            r.raise_for_status()

        # Fetching access token from Facebook failed
        except requests.exceptions.HTTPError as e:
            try:
                messages.error(request, r.json()['error']['message'])
            except ValueError:
                messages.error(request, str(e))
            return redirect(settings.LOGIN_VIEW)

        # Login with the access token from Facebook
        try:
            return store_access_token_and_redirect(
                request=request,
                access_token=self.api.facebook_login(
                    fb_access_token=r.json()['access_token'],
                ),
            )

        # Failed to login with Facebook's access token
        except self.api.APIError as e:
            logger.error(str(e))
            messages.error(request, str(e))
            return redirect(settings.LOGIN_VIEW)


class LogoutView(BaseView):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect(settings.LOGIN_VIEW)


class ResetPasswordView(BaseView):
    form_class = ResetPasswordForm
    template_name = 'auth/reset-password.html'

    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Reset the password
        try:
            self.api.reset_password(
                email=form.cleaned_data['email'],
            )

            # Push success message and redirect to the login view
            messages.success(request, 'We have sent an email with further instructions '
                                      'on how to reset your password to your email address.')
            return redirect('auth:login')

        # Registering failed
        except self.api.APIError as e:
            logger.error(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        return super(ResetPasswordView, self)._render(
            request=request,
            form=form,
            title='Reset Password',
        )
