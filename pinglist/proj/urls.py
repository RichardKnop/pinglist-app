from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/', include('apps.auth.urls', namespace='auth')),
    url(r'^alarms/', include('apps.alarms.urls', namespace='alarms')),
    url(r'^teams/', include('apps.teams.urls', namespace='teams')),
    url(r'^subscriptions/', include('apps.subscriptions.urls', namespace='subscriptions')),
    url(r'^payment-sources/', include('apps.payment_sources.urls', namespace='payment_sources')),
    url(r'^profile/', include('apps.profile.urls', namespace='profile')),
    url(r'^', include('apps.home.urls', namespace='home')),
]
