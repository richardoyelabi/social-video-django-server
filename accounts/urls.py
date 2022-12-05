from django.urls import path, include
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView,
)
from accounts.views import ProfileView, MyIdView

urlpatterns = [
    #Dj_rest_auth login and signup
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path("signup/", include("dj_rest_auth.registration.urls"),),

    #Profile
    path("<uuid:id>/", ProfileView.as_view(), name="profile"),
    path("my-id/", MyIdView.as_view(), name="my-profile-url"),
]