from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

admin.site.register(User)
