from django.urls import path, include
from rest_framework.routers import SimpleRouter

from favorite.views import FavoriteView

router = SimpleRouter()
router.register('favorites', FavoriteView)


urlpatterns = [
    path('', include(router.urls))
]
