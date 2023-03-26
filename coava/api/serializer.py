from rest_framework import serializers
from .models import User
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