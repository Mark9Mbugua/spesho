from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import *


urlpatterns = [
    path('signup', UserCreate.as_view(), name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    path('reset/password_reset/', PasswordResetView.as_view(),
         {'template_name': 'templates/registration/password_reset_email.html',
          'html_email_template_name': 'templates/registration/password_reset_email.html',
          'subject_template_name': 'templates/registration/password_reset_subject.txt',
          'from_email': 'rentor@noreply.com',
          'extra_email_context': 'templates/registration/password_reset_email.txt',
          },
         name='password_reset'),
    path('password/reset/done', PasswordResetDoneView.as_view(),
         {'template_name': 'templates/registration/password_reset_done.html'},
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         {'template_name': 'templates/registration/password_reset_complete.html'},
         name='password_reset_complete'),
    path('user/change_password', ChangePasswordView.as_view(), name="change_password"),
    path('user/profile', ProfileView.as_view(), name='user-profile'),
    path('user/update/phone-number', UpdatePhoneNumberView.as_view(), name="create_update_phone_number"),
    path('user/verification-code', VerificationCodeView.as_view(), name="verification_code"),

]
