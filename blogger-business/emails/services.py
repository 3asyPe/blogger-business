import threading

from .models import EmailActivation


class EmailActivationThread(threading.Thread):
    def __init__(self, email_activation_obj: EmailActivation, password=None):
        self.email_activation_obj = email_activation_obj
        self.password = password
        threading.Thread.__init__(self)

    def run (self):
        print("sending email")
        self.email_activation_obj.send_activation(password=self.password)


def verification_email_is_sent(user, email):
    qs = EmailActivation.objects.confirmable().filter(user=user, email=email)
    if qs.exists():
        return True
    return False


def send_verification_for_new_email(user, email):
    email_activation_obj = EmailActivation.objects.create(user=user, email=email, email_change=True)
    EmailActivationThread(email_activation_obj=email_activation_obj).start()


def send_password_email(user, email, password):
    email_activation_obj = EmailActivation.objects.create(user=user, email=email)
    EmailActivationThread(email_activation_obj=email_activation_obj, password=password).start()


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
