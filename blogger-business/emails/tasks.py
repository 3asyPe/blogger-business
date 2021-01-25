from celery import shared_task

from .models import EmailActivation


@shared_task
def send_activation_email_task(email_activation_id, password=None, *args, **kwargs):
    print(email_activation_id)
    print(EmailActivation.objects.confirmable())
    qs = EmailActivation.objects.confirmable().filter(id=email_activation_id)
    if not qs.exists():
        raise EmailActivation.DoesNotExist()
    email_activation = qs.first()
    email_activation.send_activation(password=password)
    return True
