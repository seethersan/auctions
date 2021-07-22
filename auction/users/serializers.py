from rest_framework import serializers
from users.models import UserDetails
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name',)

class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    def validate(self, data):
        if data['max_bid'] <= 1:
            raise serializers.ValidationError({"max_bid": "must a valid number"})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user_obj, created = User.objects.get_or_create(**user_data)

        user_details = UserDetails.objects.create(user=user_obj, **validated_data)
        return user_details

    def update(self, instance, validated_data):
        if validated_data.get('user', None):
            user_data = validated_data.pop('user')
            user_obj, user = User.objects.get_or_create(**user_data)

        instance.balance = validated_data['balance']
        instance.cellphone = validated_data['cellphone']
        instance.address = validated_data['address']
        instance.town = validated_data['town']
        instance.postal_code = validated_data['postal_code']
        instance.country = validated_data['country']
        instance.max_bid = validated_data['max_bid']
        return instance

    class Meta:
        model = UserDetails
        fields = ('user', 'balance', 'cellphone', 'address', 'town', 'postal_code', 'country', 'max_bid',)