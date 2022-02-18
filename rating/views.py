from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rating.models import Rating
from rating.permission import IsAuthor
from rating.serializers import RatingSerializer


class RatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        # создавать может пост авторизованный пользователь
        if self.action == 'create':
            return [IsAuthenticated()]
        # изменять и удалять может только автор поста
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]

