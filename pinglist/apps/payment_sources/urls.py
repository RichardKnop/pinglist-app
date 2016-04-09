from django.conf.urls import url

from apps.payment_sources.views import IndexView


urlpatterns = [
    url(r'^', IndexView.as_view(), name='index'),
]