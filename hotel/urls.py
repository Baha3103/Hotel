from rest_framework.routers import SimpleRouter
from django.urls import path, include

from hotel.views import HotelView, BookingView, CommentView

router = SimpleRouter()
router.register('hotel', HotelView)
router.register('booking', BookingView)
router.register('comment', CommentView)


urlpatterns = [
    path('', include(router.urls))
]
