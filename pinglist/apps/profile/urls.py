from django.conf.urls import url

from apps.profile.views import MeView


urlpatterns = [
    url(r'^', MeView.as_view(), name='me'),
]