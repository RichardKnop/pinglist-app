from django.conf.urls import url

from apps.settings.views import (
    IndexView,
    ChangePasswordView,
)


urlpatterns = [
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^$', IndexView.as_view(), name='index'),
]
