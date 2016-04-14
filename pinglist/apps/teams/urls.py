from django.conf.urls import url

from apps.teams.views import (
    IndexView,
    AddView,
    UpdateView,
    DeleteView,
)


urlpatterns = [
    url(r'^delete/(?P<team_id>[0-9]+)/$', DeleteView.as_view(), name='delete'),
    url(r'^update/(?P<team_id>[0-9]+)/$', UpdateView.as_view(), name='update'),
    url(r'^add/$', AddView.as_view(), name='add'),
    url(r'^$', IndexView.as_view(), name='index'),
]