# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.core.mail import send_mail
# from django.db import models
#
#
# class UserManager(BaseUserManager):
#     def _create(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email не может быть пустым')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_user(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_active', False)
#         extra_fields.setdefault('is_staff', False)
#         return self._create(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         return self._create(email, password, **extra_fields)
#
#
# class User(AbstractBaseUser):
#     email = models.EmailField(primary_key=True)
#     name = models.CharField(max_length=50, blank=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=8, blank=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email
#
#     def has_module_perms(self, app_label):
#         return self.is_staff
#
#     def has_perm(self, obj=None):
#         return self.is_staff
#
#     def generate_activation_code(self):
#         from django.utils.crypto import get_random_string
#
#         code = get_random_string(8)
#         self.activation_code = code
#         self.save()
#         return code
#
#     def check_token(self, token):
#         if self.activation_code == token:
#             return True
#         return False
#
#
#
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        import hashlib
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

    def create_activation_mobile(self):
        code = get_random_string(length=6, allowed_chars='123456789')
        self.activation_code = code

    def __str__(self):
        return f'{self.username} {self.email}'