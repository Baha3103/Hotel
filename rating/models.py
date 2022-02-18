from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from hotel.models import Hotel

User = get_user_model()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    star = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], default=0)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return f"{self.star}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        # unique_together = ['hotel', 'user']
