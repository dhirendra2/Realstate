import django.contrib.auth.password_validation as validators
from django.core import exceptions 
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import jwt 

from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('__all__')
   
class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    password = serializers.CharField(source="user.password", write_only=True)
    role = serializers.CharField(source="user.role", required=False)
    token = serializers.SerializerMethodField("get_token")

    def get_token(self, obj):

        try:
            return obj.token
        except:
            return ""

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "token",
            "is_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, validated_data):
        # here data has all the fields which have validated values

        status = False
        try:
            if "password" in validated_data["user"]:
                status = True

        except:
            status = False

        if status:

            password = (validated_data["user"])["password"]

            errors = dict()
            try:
                # validate the password and catch the exception
                validators.validate_password(password=password)

            # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)

            if errors:
                raise serializers.ValidationError(errors)

            (validated_data["user"])["password"] = make_password(password)

        return validated_data

    def create(self, validated_data):
        """
        Creating a django user
        """

        object_instance = None
        (validated_data["user"])["username"] = (validated_data["user"])["email"]

        if "is_password" not in validated_data:
            validated_data["is_password"] = True

        serializer = UserSerializer(data=validated_data["user"])
        if serializer.is_valid(raise_exception=True):
            object_instance = serializer.save()

        validated_data["user"] = object_instance
        return UserProfile.objects.create(**validated_data)
