from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


# Модель отеля
class Hotel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    location = models.TextField(blank=True, null=True)
    visitorCount = models.IntegerField(blank=True, null=True, default=0)
    cost = models.FloatField(blank=True, null=True)
    stars = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    likes = GenericRelation('Like', blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_user_email')

    def __str__(self):
        return self.name

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class HotelImage(models.Model):
    hotel_image = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='pics')
    image = models.ImageField(upload_to='hotels')


# статусы бронирования отеля
STATUS_CHOICES = (
    ('OPEN', 'Открыт'),
    ('BOOKED', 'Забронирован')
)


# Модель бронирование отеля
class BookingModels(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='booking')
    customer_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    customer_phonenumber = models.CharField(max_length=20, blank=True, null=True)
    # customer_email = models.ForeignKey(Hotel, on_delete=models.RESTRICT)
    time = models.DateField(auto_now_add=True)
    amount = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[1][1])
    checkInDate = models.DateField(auto_now_add=True, blank=True, null=True)
    checkOutDate = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.hotel_id.name

    class Meta:
        verbose_name = "Booking"


# Модель комментариев
class Comment(models.Model):
    hotel = models.ForeignKey(Hotel,
                              on_delete=models.CASCADE,
                              related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.name

