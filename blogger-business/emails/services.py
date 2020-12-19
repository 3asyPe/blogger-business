from .models import EmailActivation


def send_password_email(user, email, password):
    email_activation_obj = EmailActivation.objects.create(user=user, email=email)
    return email_activation_obj.send_activation(password=password)


def activate_email_and_get_redirect_url(key):
    email_activation_obj = EmailActivation.objects.get(key__iexact=key)
    if email_activation_obj.can_activate():
        email_activation_obj.activate()
        redirect = "/login?activated"
    elif email_activation_obj.activated:
        redirect = "/login/"
    else:
        redirect = None
    
    return redirect


def reactivate_email_and_get_response_data(email):
    qs = EmailActivation.objects.email_exists(email=email)
    if not qs.exists():
        message = "Account with this email doesn't exist"
        status = 404
        return message, status

    activated = qs.filter(activated=True)
    if activated.exists():
        message = "This email is already activated"
        status = 409
        return message, status
    
    email_activation_obj = qs.first()
    user = email_activation_obj.user
    new_activation = EmailActivation.objects.create(user=user, email=email)
    new_activation.send_activation()
    
    message = "The activation email was sent"
    status = 200
    return message, status
