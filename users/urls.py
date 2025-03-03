from django.urls import path

from .views import (ChangeUserStatusView, CustomLoginView, CustomLogoutView, EditProfileUpdateView,
                    PasswordResetConfirmView, PasswordResetRequestView, RegisterView, UserProfileDetailView,
                    UsersListView, email_verification)

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("all-users/", UsersListView.as_view(), name="all-users"),
    path("user-profile/<int:pk>/", UserProfileDetailView.as_view(), name="user-profile"),
    path("edit-profile/<int:pk>/", EditProfileUpdateView.as_view(), name="edit-profile"),
    path("change-status/<int:pk>/", ChangeUserStatusView.as_view(), name="change-status"),
    path("reset-password/", PasswordResetRequestView.as_view(), name="reset-password"),
    path("reset-password-confirm/<str:token>/", PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
]
