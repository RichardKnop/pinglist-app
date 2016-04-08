from django.conf.urls import url

from apps.dashboard.views.login import LoginView
from apps.dashboard.views.logout import LogoutView
from apps.dashboard.views.facebook_redirect import FacebookRedirectView
from apps.dashboard.views.subscriptions import SubscriptionsView
from apps.dashboard.views.payment_sources import PaymentSourcesView
from apps.dashboard.views.profile import ProfileView


urlpatterns = [
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^facebook-redirect', FacebookRedirectView.as_view(), name='facebook_redirect'),
    url(r'^subscriptions', SubscriptionsView.as_view(), name='subscriptions'),
    url(r'^payment-sources', PaymentSourcesView.as_view(), name='payment_sources'),
    url(r'^profile', ProfileView.as_view(), name='profile'),
]