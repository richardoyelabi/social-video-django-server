from django.urls import path, re_path, include
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from accounts.views import ProfileView, MyIdView

urlpatterns = [
    # Dj_rest_auth login and signup
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path(
        "signup/",
        include("dj_rest_auth.registration.urls"),
    ),
    # Dj_rest_auth email verification
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    # Profile
    path("<uuid:id>/", ProfileView.as_view(), name="profile"),
    path("my-id/", MyIdView.as_view(), name="my-id"),
]
