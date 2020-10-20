from django.shortcuts import render
from django.http import Http404

from .models import Blogger


def profile_view(request, blogger_id):
    try:
         blogger = Blogger.objects.get(id=blogger_id)
    except Blogger.DoesNotExist:
        return Http404(f"Blogger with id-{blogger_id} doesn't exist")
    context = {
        "blogger": blogger,
    }
    return render(request, "blogger/profile.html", context)

