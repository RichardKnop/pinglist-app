from django.conf.urls import url

from apps.alarms.views import (
    IndexView,
    AddView,
    UpdateView,
)


urlpatterns = [
    url(r'^update/(?P<alarm_id>[0-9]+)/$', UpdateView.as_view(), name='update'),
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]