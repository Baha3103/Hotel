from django.contrib.auth import get_user_model
from rest_framework import serializers

from hotel.models import Hotel, BookingModels, Comment, HotelImage
from rating.serializers import RatingSerializer

User = get_user_model()


class HotelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    # is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'location', 'visitorCount', 'cost', 'stars', 'image', 'total_likes')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_data = RatingSerializer(instance.ratings.all(), many=True).data
        total = 0
        for ord in rating_data:
            total += ord.get('star')
            representation['rating'] = total / len(rating_data)
        return representation

    def get_image(self, request):
        first_image = request.pics.first()
        if first_image and first_image.image:
            return first_image.image.url  # если image есть вернет URL
        return ''  # если image то вернет пустую строку

    # def get_is_fan(self, obj) -> bool:
    #     """Check if a `request.user` has liked this tweet (`obj`).
    #     """
    #     user = self.context.get('request').user
    #     return hotel_services.is_fan(obj, user)


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        exclude = ['likes']


class HotelsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False), write_only=True,
                                   required=False)

    class Meta:
        model = Hotel
        exclude = ['user', 'likes']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        images = validated_data.pop('images', [])
        post = super().create(validated_data)
        for image in images:
            HotelImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])  # по default пустой список
        if images:
            for image in images:
                HotelImage.objects.create(post=instance, image=image)
        return super().update(instance, validated_data)

    # def is_liked(self, hotel):
    #     user = self.context.get('request').user
    #     user.liked.filter(hotel=hotel).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = HotelImageSerializer(instance.pics.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.favorites.count()
        return representation


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingModels
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name',
                  'full_name')
