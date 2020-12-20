import math

from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from .utils import create_activation_key
from account.models import User


DEFAULT_ACTIVATION_DAYS = getattr(settings, "DEFAULT_EMAIL_ACTIVATION_EXPIRE_DAYS", 1)


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False,
            timestamp__gt=start_range,
            timestamp__lte=end_range,
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email) | Q(user__email=email)
        )


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    email_change = models.BooleanField(default=False)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is None:
            return True
        return False

    def hours_to_expire_left(self):
        now = timezone.now()
        expire = self.timestamp + timedelta(days=DEFAULT_ACTIVATION_DAYS)
        time_left = expire - now
        hours = math.ceil(time_left.seconds / 3600)
        return hours

    def send_activation(self, password=None):
        if not self.activated and not self.forced_expired and self.key:
            domain = getattr(settings, "DOMAIN_NAME", "https://www.bloggerbusiness.org/")
            key_path = reverse("emails:activate-email", kwargs={"key": self.key})
            path = f"{domain}{key_path}"
            context = {
                "domain": domain,
                "email": self.email,
                "path": path,
                "password": password,
            }
            
            if not self.email_change:
                txt_ = get_template("registration/email/verify.txt").render(context)
                html_ = get_template("registration/email/verify.html").render(context)
                subject = "Account activation"
            else:
                txt_ = get_template("registration/email/change_verify.txt").render(context)
                html_ = get_template("registration/email/change_verify.html").render(context)
                subject = "Email confirmation"
                
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "BLOGGER&BUSINESS <bloggerandbusiness@gmail.com>")
            recipient_list = [self.email]

            sent_mail = send_mail(
                subject=subject,
                message=txt_,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_,
                fail_silently=False
            )

            print("Email has been sent")

            return sent_mail

        return False


def pre_save_email_activation_receiver(sender, instance: EmailActivation, *args, **kwargs):
    if not instance.activated and not instance.forced_expired and not instance.key:
        create_activation_key(instance, type(instance))


pre_save.connect(pre_save_email_activation_receiver, sender=EmailActivation)


def post_save_create_email_activation_receiver(sender, instance: EmailActivation, created, *args, **kwargs):
    if created:
        qs = EmailActivation.objects.confirmable().filter(user=instance.user).exclude(id=instance.id)
        for obj in qs:
            obj.forced_expired = True
            obj.save()


post_save.connect(post_save_create_email_activation_receiver, sender=EmailActivation)
