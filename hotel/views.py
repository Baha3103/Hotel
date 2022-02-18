from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.shortcuts import get_object_or_404

from favorite.models import Favorites
from hotel import services
from hotel.models import Hotel, BookingModels, Comment, Like
from hotel.permission import IsAuthor
from hotel.serializers import HotelSerializer, BookingSerializer, CommentSerializer, FanSerializer


class HotelView(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']  # поиск по названию
    ordering_fields = ['name', 'cost', 'location']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Hotel, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['is_liked'] = liked
        return data

    # def get_permissions(self):
    #     # создавать может пост авторизованный пользователь
    #     if self.action in ['create', 'add_to_favorites', 'remove_from_favorites']:
    #         return [IsAuthenticated()]
    #     # изменять и удалять модет только автор поста
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         return [IsAuthor()]
    #     # просмотр поста доступен всем
    #     return []

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'list':
            serializer_class = HotelSerializer
        return serializer_class

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk=None):
        hotel = self.get_object()
        data = Favorites.objects.all()
        for favorite in data:
            if favorite.hotel.id == hotel.id:
                if favorite.user.email == request.user.email:
                    return Response('Уже добавлено в избранное')
        Favorites.objects.create(hotel=hotel, user=request.user)
        return Response('Добавлено в избранное')

    @action(['DELETE'], detail=True)
    def remove_from_favorites(self, request, pk=None):
        hotel = self.get_object()
        data = Favorites.objects.all()
        for favorite in data:
            if favorite.hotel.id == hotel.id:
                if favorite.user.email == request.user.email:
                    favorite.delete()
                    return Response('Удален из избранных')
        return Response('Невозможно удалить, так как нет в избранных')

    @action(['GET'], detail=False)
    def favoritlist(self, request):
        res = []
        data = request.user.liked.all()
        for hot in data:
            res.append(hot.hotel)
        serializer = HotelSerializer(res, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        """Лайкает `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(['POST'], detail=True)
    def unlike(self, request, pk=None):
        """Удаляет лайк с `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    # @action(['GET'], detail=False)
    # def fans(self, request, pk=None):
    #     """Получает всех пользователей, которые лайкнули `obj`.
    #     """
    #     obj = self.get_object()
    #     fans = services.get_fans(obj)
    #     serializer = FanSerializer(fans, many=True)
    #     return Response(serializer.data)


class BookingView(ModelViewSet):
    queryset = BookingModels.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['customer_name', 'status', 'checkOutDate']
    ordering_fields = ['customer_name']


class CommentView(CreateModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        # создавать может пост авторизованный пользователь
        if self.action == 'create':
            return [IsAuthenticated()]
        # изменять и удалять может только автор поста
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
