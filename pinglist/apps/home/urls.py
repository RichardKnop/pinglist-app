from django.conf.urls import url

from apps.home.views import (
    IndexView,
    FAQView,
    ContactView,
)


urlpatterns = [
    url(r'^contact', ContactView.as_view(), name='contact'),
    url(r'^faq', FAQView.as_view(), name='faq'),
    url(r'^$', IndexView.as_view(), name='index'),
]