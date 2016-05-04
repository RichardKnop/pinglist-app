from django.conf.urls import url

from apps.alarms.views import (
    IndexView,
    AddView,
    UpdateView,
    DeleteView,
    AlarmIncidentsView,
    AlarmMetricsView,
)


urlpatterns = [
    url(r'^(?P<alarm_id>[0-9]+)/metrics/$', AlarmMetricsView.as_view(), name='alarm_metrics'),
    url(r'^(?P<alarm_id>[0-9]+)/incidents/$', AlarmIncidentsView.as_view(), name='alarm_incidents'),
    url(r'^delete/(?P<alarm_id>[0-9]+)/$', DeleteView.as_view(), name='delete'),
    url(r'^update/(?P<alarm_id>[0-9]+)/$', UpdateView.as_view(), name='update'),
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]
