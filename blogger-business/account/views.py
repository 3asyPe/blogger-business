from django.shortcuts import render


def registration_view(request):
    account_type = request.GET.get("type")
    if account_type == "bl":
        pass
    elif account_type == "bu":
        pass

 