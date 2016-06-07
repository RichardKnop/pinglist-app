from django.conf.urls import url

from apps.subscriptions.views import (
    IndexView,
    AddView,
    UpdateView,
    CancelView,
)


urlpatterns = [
    url(r'^cancel/(?P<subscription_id>[0-9]+)/$', CancelView.as_view(), name='cancel'),
    url(r'^update/(?P<subscription_id>[0-9]+)/$', UpdateView.as_view(), name='update'),
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]
