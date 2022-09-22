from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import Profile

# from rest_framework.serializers import Serializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "note"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile"]

    def update(self, instance, validated_data):
        profile = validated_data.pop("profile")
        profile_seri = ProfileSerializer(instance.profile, data=profile)
        profile_seri.is_valid(raise_exception=True)
        profile_seri.save()
        return super(UserSerializer, self).update(instance, validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

        def validate(self, attr):  # indent
            validate_password(attr["password"])
            return attr

        def create(self, validated_data):
            user = User.objects.create(username=validated_data["username"])
            user.set_password(validated_data["password"])
            user.save()
            return user


# class ChangePwd(Serializer):
#     old_pwd = serializers.CharField(required=True)
#     new_pwd = serializers.CharField(required=True)

#     def validate_new_pwd(self, value):
#         validate_password(value)
#         return value
