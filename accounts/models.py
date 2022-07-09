from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


# Create your models here.
from django.shortcuts import resolve_url
from django.template.loader import render_to_string


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")], blank=True)
    gender =models.CharField(max_length=1 ,choices=GenderChoices.choices, blank=True)
    # TODO : [Jay_Lee] Avatar Validator Check - 기준 : Help_text
    avatar = models.ImageField(blank=True, upload_to='accounts/profile/%Y/%m/%d',
                               help_text="48 px * 48 px 크기의 jpg/png 를 업로드 해주세요.")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)

    def send_welcome_email(self):
        pass
        # # 여러줄 사용을 없애기 위해 Template를 활용한다.
        # subject = render_to_string("accounts/welcome_email_subject.txt", {
        #     "user": self,
        # })
        # content = render_to_string("accounts/welcome_email_content.txt", {
        #     "user": self,
        # })
        # sender_email = settings.WELCOME_EMAIL_SENDER
        # send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # def save(self, *args, **kwargs):
    #     is_created = (self.pk == None)
    #     super().save(*args, **kwargs)


# class Profile(models.Model):
#     pass
