from django.conf.urls import url

from apps.dashboard.views.index import IndexView
from apps.dashboard.views.sign_in import SignInView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^sign-in', SignInView.as_view(), name='sign_in'),
]
