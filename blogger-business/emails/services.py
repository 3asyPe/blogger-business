from .models import EmailActivation


def send_verification_for_new_email(user, email):
    email_activation_obj = EmailActivation.objects.create(user=user, email=email, email_change=True)
    return email_activation_obj.send_activation()


def send_password_email(user, email, password):
    email_activation_obj = EmailActivation.objects.create(user=user, email=email)
    return email_activation_obj.send_activation(password=password)


def activate_email_and_get_redirect_url(key):
    email_activation_obj = EmailActivation.objects.get(key__iexact=key)
    if email_activation_obj.can_activate():
        email_activation_obj.activate()
        user = email_activation_obj.user
        email = email_activation_obj.email
        if user.email != email:
            _change_user_email(user=user, email=email)
            redirect = "/profile?confirmed"
        else:
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


def _change_user_email(user, email: str):
    user.email = email
    if user.is_blogger:
        user.blogger.email = email
        user.blogger.save()
    if user.is_business:
        user.business.email = email
        user.business.save()
    user.save()
