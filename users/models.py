from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    email = models.EmailField()
    # password = models. To be completed
    is_an_elder = models.BooleanField()
    birthday = models.CharField(max_length=120)
    # hobbies = models.To be completed
    # languages = models. To be completed
    linked_user = models.CharField(max_length=120)
    gps_location = models.CharField(max_length=120)

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, name, phone, is_an_elder, birthdate, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not name:
            raise ValueError("Users must fill in their name")
        if not phone:
            raise ValueError("Users must insert their phone number")
        if is_an_elder==None :
            raise ValueError("Users must specify the type of account they are creating.")
        if not birthdate:
            raise ValueError("Users must register the date of birth")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
            phone = phone,
            is_an_elder = is_an_elder,
            birthdate = birthdate,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, username, name, phone, is_an_elder, birthdate, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            name = name,
            phone = phone,
            is_an_elder = is_an_elder,
            birthdate = birthdate,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50, verbose_name="name")
    phone = models.CharField(max_length=20, verbose_name="phone number")
    is_an_elder = models.BooleanField()
    birthdate = models.DateField(max_length=120, verbose_name="date of birth")
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'name', 'phone', 'is_an_elder', 'birthdate']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# Create your models here.
