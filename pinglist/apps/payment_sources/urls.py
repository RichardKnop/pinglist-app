from django.conf.urls import url

from apps.payment_sources.views import (
    IndexView,
    AddView,
    DeleteView,
)


urlpatterns = [
    url(r'^delete/(?P<card_id>[0-9]+)/$', DeleteView.as_view(), name='delete'),
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]