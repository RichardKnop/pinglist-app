from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from apps.dashboard.forms.sign_in import SignInForm
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from . import HTML_TITLE


class SignInView(View):
    form_class = SignInForm
    initial = {}
    template_name = 'dashboard/sign-in.html'
    oauth = OAuth2Session(
        client=LegacyApplicationClient(
            client_id=settings.OAUTH_CLIENT_ID,
        ),
    )

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)
        try:
            token = self.oauth.fetch_token(
                token_url=settings.OAUTH_TOKEN_URL,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                client_id=settings.OAUTH_CLIENT_ID,
                client_secret=settings.OAUTH_CLIENT_SECRET,
            )
            print token
        except Exception as e:
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        return HttpResponse(
            render(
                request,
                self.template_name,
                {
                    'title': HTML_TITLE,
                    'form': form,
                },
            )
        )
