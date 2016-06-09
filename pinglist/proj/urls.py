from django.conf.urls import include, url
from django.utils.functional import curry
from django.views.defaults import *

handler404 = curry(server_error, template_name='404.html')
handler500 = curry(server_error, template_name='500.html')

urlpatterns = [
    url(r'^captcha/', include('captcha.urls')),
    url(r'^auth/', include('apps.auth.urls', namespace='auth')),
    url(r'^web/', include('apps.web.urls', namespace='web')),
    url(r'^alarms/', include('apps.alarms.urls', namespace='alarms')),
    url(r'^teams/', include('apps.teams.urls', namespace='teams')),
    url(r'^subscriptions/', include('apps.subscriptions.urls', namespace='subscriptions')),
    url(r'^payment-sources/', include('apps.payment_sources.urls', namespace='payment_sources')),
    url(r'^settings/', include('apps.settings.urls', namespace='settings')),
    url(r'^', include('apps.home.urls', namespace='home')),
]
