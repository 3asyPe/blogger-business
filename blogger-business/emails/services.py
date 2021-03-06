import threading

from django.db import transaction

from .models import EmailActivation
from .tasks import send_activation_email_task


class EmailActivationRunner:
    def __init__(self, email_activation_obj: EmailActivation, password=None):
        self.email_activation_obj = email_activation_obj
        self.password = password

    def run(self):
        send_activation_email_task.delay(email_activation_id=self.email_activation_obj.id, password=self.password)


def verification_email_is_sent(user, email):
    qs = EmailActivation.objects.confirmable().filter(user=user, email=email)
    if qs.exists():
        return True
    return False


def create_change_email_activation(user, email) -> EmailActivationRunner:
    email_activation_obj = EmailActivation.objects.create(user=user, email=email, email_change=True)
    email_activation_runner = EmailActivationRunner(email_activation_obj=email_activation_obj)
    return email_activation_runner


def create_password_email_activation(user, email, password) -> EmailActivationRunner:
    email_activation_obj = EmailActivation.objects.create(user=user, email=email)
    email_activation_runner = EmailActivationRunner(email_activation_obj=email_activation_obj, password=password)
    return email_activation_runner


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
    activation_runner = create_change_email_activation(user=user, email=email)
    activation_runner.run()
    
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
