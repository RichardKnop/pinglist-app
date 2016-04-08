from django.conf.urls import url

from apps.dashboard.views.login import LoginView
from apps.dashboard.views.logout import LogoutView
from apps.dashboard.views.facebook_redirect import FacebookRedirectView
from apps.dashboard.views.subscriptions import SubscriptionsView


urlpatterns = [
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^facebook-redirect', FacebookRedirectView.as_view(), name='facebook_redirect'),
    url(r'^subscriptions', SubscriptionsView.as_view(), name='subscriptions'),
]