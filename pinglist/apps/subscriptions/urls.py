from django.conf.urls import url

from apps.subscriptions.views import (
    IndexView,
    AddView
)


urlpatterns = [
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]