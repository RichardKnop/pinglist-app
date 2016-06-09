from django.conf.urls import url

from apps.web.views import (
    ConfirmEmailView,
    ConfirmInvitationView,
    ConfirmPasswordResetView,
    ConfirmInvitationSuccessView,
    ConfirmPasswordResetSuccessView,
)


urlpatterns = [
    url(r'^confirm-email/(?P<reference>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ConfirmEmailView.as_view(), name='confirm_email'),
    url(r'^confirm-invitation/(?P<reference>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ConfirmInvitationView.as_view(), name='confirm_invitation'),
    url(r'^confirm-password-reset/(?P<reference>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ConfirmPasswordResetView.as_view(), name='confirm_password_reset'),
    url(r'^confirm-invitation-success/$', ConfirmInvitationSuccessView.as_view(), name='confirm_invitation_success'),
    url(r'^confirm-password-reset-success/$', ConfirmPasswordResetSuccessView.as_view(), name='confirm_password_reset_success'),
]
