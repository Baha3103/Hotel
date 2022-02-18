from rest_framework.routers import SimpleRouter
from django.urls import path, include

from rating.views import RatingView

router = SimpleRouter()
router.register('rating', RatingView)

urlpatterns = [
    path('', include(router.urls))
]

