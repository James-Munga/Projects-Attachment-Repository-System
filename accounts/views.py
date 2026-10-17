from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core import signing
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import RegistrationForm
from .models import UserProfile

TOKEN_SALT = "accounts.email-verification"

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"].lower()
            user.set_password(form.cleaned_data["password"])
            user.save()
            token = signing.dumps({"user_id": user.pk, "email": user.email}, salt=TOKEN_SALT)
            verify_url = settings.SITE_URL + reverse("verify-email", args=[token])
            send_mail(
                "Verify your Project Attachments account",
                f"Hello {user.first_name or user.username},\\n\\nVerify your email using this link:\\n{verify_url}\\n\\nIf you did not create this account, you can ignore this email.",
                settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False,
            )
            return render(request, "accounts/registration_sent.html", {"email": user.email})
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def verify_email(request, token):
    try:
        payload = signing.loads(token, salt=TOKEN_SALT, max_age=60 * 60 * 24)
        user = User.objects.get(pk=payload["user_id"], email=payload["email"])
        profile = user.userprofile
    except (signing.BadSignature, signing.SignatureExpired, User.DoesNotExist, UserProfile.DoesNotExist, KeyError):
        messages.error(request, "This verification link is invalid or has expired. Please contact an administrator.")
        return redirect("login")
    profile.email_verified = True
    profile.save(update_fields=["email_verified"])
    messages.success(request, "Email verified. An administrator must approve your account before you can access project materials.")
    return redirect("login")
