from django.shortcuts import render, redirect

from .models import EmailActivation
from .services import (
    activate_email_and_get_redirect_url,
    reactivate_email_and_get_response_data,
)

from rest_framework.decorators import api_view
from rest_framework.response import Response


def email_activation_view(request, key):
    try:
        redirect_url = activate_email_and_get_redirect_url(key=key)
    except EmailActivation.DoesNotExist:
        print("error")
        return render(request, "registration/activation_error.html", {})

    if redirect_url is None:
        return render(request, "registration/activation_error.html", {})

    return redirect(redirect_url)


@api_view(["POST"])
def email_reactivation(request):
    print(request.POST)
    try:
        email = request.POST["email"]
    except KeyError:
        return Response({"message": "Data object doesn't have an email field"}, status=400)

    message, status = reactivate_email_and_get_response_data(email=email)

    return Response({"message": message}, status=status)
