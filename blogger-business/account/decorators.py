from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return view_func(request, *args, **kwargs)
        elif user.is_blogger:
            return redirect("/dashboard/")
        elif user.is_business:
            return redirect("/offers/actions")
        raise ValueError("User account neither blogger or business")

    return wrapper_func


def allowed_users(allowed_roles:list=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            roles = []
            for role in allowed_roles:
                roles.append(role.lower())
            if not user.is_authenticated:
                return redirect("/login/")
            if user.is_blogger and "blogger" in roles:
                return view_func(request, *args, **kwargs)
            if user.is_business and "business" in roles:
                return view_func(request, *args, **kwargs)
            return redirect("/login/")
            
        return wrapper_func
    return decorator