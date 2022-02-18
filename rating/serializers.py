from rest_framework import serializers

from rating.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['user']   #исключаем user

    def validate(self, attrs):
        user = self.context.get('request').user
        hotel = attrs.get('hotel')
        if user.ratings.filter(hotel=hotel).exists():
            raise serializers.ValidationError('Вы уже поставили рейтинг')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
