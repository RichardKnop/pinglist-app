from django.conf.urls import url

from apps.auth.views import (
    RegisterView,
    LoginView,
    FacebookRedirectView,
    LogoutView,
)


urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^facebook-redirect/', FacebookRedirectView.as_view(), name='facebook_redirect'),
]