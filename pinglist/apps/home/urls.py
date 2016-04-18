from django.conf.urls import url

from apps.home.views import (
    IndexView,
    TermsView,
    ContactView,
)


urlpatterns = [
    url(r'^contact', ContactView.as_view(), name='contact'),
    url(r'^terms$', TermsView.as_view(), name='terms'),
    url(r'^$', IndexView.as_view(), name='index'),
]