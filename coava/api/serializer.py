from rest_framework import serializers
from .models import *
from argon2 import PasswordHasher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            ph = PasswordHasher() # 비밀번호 암호화
            hash = ph.hash(instance.password.encode())
            instance.password = hash
        instance.save()
        return instance

class DailySerializer(serializers.ModelSerializer): #출석체크
    class Meta:
        model = Daily
        fields = ("__all__")

class MemeSerializer(serializers.ModelSerializer): #밈
    class Meta:
        model = Meme
        fields = ("__all__")

class BuzzSerializer(serializers.ModelSerializer): #유행어
    class Meta: 
        model = Buzz
        fields = ("__all__")

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("__all__")

class MyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyItem
        fields = ("__all__")