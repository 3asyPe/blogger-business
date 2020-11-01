from django.shortcuts import render

from account.decorators import allowed_users

from rest_framework.decorators import api_view


@allowed_users(["BUSINESS"])
def applications_view(request):
    return render(request, "application/applications.html", {})



