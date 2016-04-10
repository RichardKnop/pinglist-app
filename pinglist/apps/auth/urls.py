from django.conf.urls import url

from apps.auth.views import (
    LoginView,
    FacebookRedirectView,
    LogoutView
)


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^facebook-redirect/', FacebookRedirectView.as_view(), name='facebook_redirect'),
]