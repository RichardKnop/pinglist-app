from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('apps.home.urls', namespace='home')),
    url(r'^', include('apps.dashboard.urls', namespace='dashboard')),
]
