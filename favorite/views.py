from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from favorite.models import Favorites
from favorite.permission import IsAuthor
from favorite.serializers import FavoriteSerializer


class FavoriteView(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer

    def get_permissions(self):
        # создавать может пост авторизованный пользователь
        if self.action in ['create', 'add_to_favorites', 'remove_from_favorites']:
            return [IsAuthenticated()]
        # изменять и удалять модет только автор поста
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        # просмотр поста доступен всем
        return []


