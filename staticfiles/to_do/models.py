from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomAccountManager(BaseUserManager):

    def create_personal(self, email, username, password, **other_fields):

        other_fields.setdefault('is_verified', True)
        other_fields.setdefault('is_personal', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, **other_fields)

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.'
            )

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True.'
            )

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          password=password, **other_fields)

        user.set_password(password)
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(auto_created=True, primary_key=True,
                          unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(_('Email address'), max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True)
    # telephone_number = PhoneNumberField()
    date_of_birth = models.DateField(auto_now_add=False, blank=True, null=True)

    # complete Profile
    profile_photo = models.ImageField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    physical_address = models.CharField(max_length=100, blank=True, null=True)
    # country = CountryField(blank=True, null=True)

    # More Verification
    is_active = models.BooleanField(default=False)

    # is_business = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def imageURL(self):
        try:
            url = self.profile_photo.url
        except:
            url = ''  # apps_images/logo.jpg
        return url

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return reverse("account-settings", kwargs={"pk": self.id})

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Task(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    happening_on = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}, uploaded by {self.user.username}"

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def get_absolute_url(self):
        return reverse("home")
    