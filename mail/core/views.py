import secrets

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View

from core.forms import UserForm
from core.models import ConfirmationToken

from .tasks import send_confirmation_email


class RegistrationView(View):
    def get(self, request):
        user_form = UserForm()
        context = {
            "form": user_form,
        }
        return render(request, "core/registration.html", context)

    def post(self, request):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            confirmation_token = ConfirmationToken.objects.create(
                user=user, confirmation_key=secrets.token_hex(16)
            )

            # Scheduling task for Emails
            send_confirmation_email.delay(
                confirmation_token.confirmation_key,
                user.id,
                user.email,
            )
            print("email sent")

            messages.success(request, "Registered Successfully. Check email for verification")

            return redirect("registration")

        messages.warning(
            request, "Verify your email"
        )

        context = {
            "form": user_form,
        }
        return render(request, "core/registration.html", context)


class ConfirmRegistrationView(View):
    def get(self, request):
        user_id = request.GET.get("id", None)
        confirmation_key = request.GET.get("confirmation_key", None)

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            messages.warning(request, "User does not exits....")
            return redirect("registration")

        if user.confirmation_token.is_confirmed:
            messages.warning(request, "Confirmation token is not valid.")
            return redirect("registration")

        if user.confirmation_token.confirmation_key == confirmation_key:
            user.confirmation_token.is_confirmed = True
            user.confirmation_token.save()

            messages.success(
                request, "verified successfully..."
            )
        else:
            messages.warning(request, "invalid details.")

        return redirect("registration")
