from django.urls import path

from accounts.views.auth_view import LoginView, RegisterView
from accounts.views.profile_view import ProfileView

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
]