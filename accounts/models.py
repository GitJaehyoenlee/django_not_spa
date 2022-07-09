from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings


# Create your models here.
from django.template.loader import render_to_string


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def send_welcome_email(self):
        # 여러줄 사용을 없애기 위해 Template를 활용한다.
        subject = render_to_string("accounts/welcom_email_subject.txt", {
            "user": self,
        })
        content = render_to_string("accounts/welcom_email_content.txt", {
            "user": self,
        })
        sender_email = settings.WELOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # def save(self, *args, **kwargs):
    #     is_created = (self.pk == None)
    #     super().save(*args, **kwargs)


# class Profile(models.Model):
#     pass
