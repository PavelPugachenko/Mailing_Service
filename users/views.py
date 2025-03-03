import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, EditProfileForm, PasswordResetConfirmForm, PasswordResetRequestForm
from .logger import users_logger
from .models import CustomUser
from .services import CACHE_TIMEOUT, CustomUserService


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    users_logger.info(f"User {user} confirmed email.")
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("mailing:home")


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
    next_page = reverse_lazy("users:logout")


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        users_logger.info(f"User {user} registered.")
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Email confirmation",
            message=f"Hi! Please follow the link to confirm your email {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        users_logger.info(f"Email confirmation sent to {user}.")
        return super().form_valid(form)


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = "edit_profile.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Profile updated successfully. Changes will be displayed after {CACHE_TIMEOUT} seconds."
        )
        return reverse_lazy("users:user-profile", kwargs={"pk": self.object.pk})


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "users.view_customuser"
    model = CustomUser
    template_name = "all_users.html"
    context_object_name = "users"
    queryset = CustomUserService.get_all_users().order_by("id")


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CACHE_TIMEOUT"] = CACHE_TIMEOUT
        return context


class ChangeUserStatusView(PermissionRequiredMixin, View):
    permission_required = "users.can_block_user"

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        if user == request.user:
            messages.warning(request, "You cannot block yourself.")
            return redirect("users:all-users")
        user.is_active = not user.is_active
        user.save()
        users_logger.info(f"User {user} status changed.")
        return redirect("users:all-users")


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, "password_reset_request.html", {"form": form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data["email"])
            host = self.request.get_host()
            token = secrets.token_hex(16)
            user.password_reset_token = token
            user.save()
            users_logger.info(f"User {user} requested password reset.")
            reset_url = f"{host}/users/reset-password-confirm/{token}/"
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            users_logger.info(f"Password reset request sent to {user}.")
            messages.success(request, "Password reset request sent to your email account.")
            return redirect("users:login")
        return render(request, "password_reset_request.html", {"form": form})


class PasswordResetConfirmView(View):

    def get(self, request, token):
        user = get_object_or_404(CustomUser, password_reset_token=token)
        form = PasswordResetConfirmForm()
        return render(request, "password_reset_confirm.html", {"form": form, "token": token, "email": user.email})

    def post(self, request, token):
        user = get_object_or_404(CustomUser, password_reset_token=token)
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.password_reset_token = None
            user.save()
            users_logger.info(f"User {user} password reset.")
            messages.success(request, "Your new password is successfully set.")
            return redirect("users:login")
        return render(request, "password_reset_confirm.html", {"form": form, "token": token})
