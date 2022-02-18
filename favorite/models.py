from django.contrib.auth import get_user_model
from django.db import models

from hotel.models import Hotel

User = get_user_model()


class Favorites(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['hotel', 'user']

    def __str__(self):
        return self.hotel.name


