from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import *
from .serializers import *
import logging



def get_user_profile(request):

    token = request.auth
    decoded_token = jwt.decode(str(token).encode("utf-8"), settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_token["user_id"]
    instance = UserProfile.objects.get(user__id=user_id)

    return instance


class SignUp(APIView):
    """SignUp
    this api is responsible to register new user
    Body:
        {
            "first_name": str,
            "last_name": str,
            "email": str,
            "password": str
        }
    """

    def post(self, request):
        data = request.data
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logging.info("save success")
            return Response(
                data={
                    "IsStatus": True,
                    "Data": serializer.data,
                    "Message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )


class SignIn(APIView):
    """SignIn
    this api is responsible for signin to user
    body:
        {
            "email": str,
            "password": str
        }
    """

    def post(self, request):

        data = request.data
        username = data.get("email", None)
        password = data.get("password", None)

        try:

            if username and password:
                user_profile = UserProfile.objects.get(user__username=username)
                if user_profile.user.is_active and check_password(password, user_profile.user.password):
                    login(request, user_profile.user)
                    refresh = RefreshToken.for_user(user_profile.user)
                    user_profile.token = str(refresh.access_token)
                    print(user_profile.token,"==========================")
                    serializer = UserProfileSerializer(user_profile)
                    print(serializer,"+++++++++++++++++++++++++")
                    logging.info("Sign in success")
                    return Response(data={"IsStatus": True,"Data": serializer.data,
                            "Message": "SignIn Successfully",},status=status.HTTP_200_OK,)
                else:
                    return Response(
                        data={
                            "IsStatus": False,
                            "Message": "Provided email and password is mismatch.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

            else:
                return Response(
                    data={"IsStatus": False, "Message": "Provide email and password."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            logging.error("sign in failed because : " + str(e))
            return Response(
                data={"IsStatus": False, "Message": "Invalid email or password."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def new_method(self, request, username, password):
        user = authenticate(request, username=username, password=password) 
        
        
class Logout(APIView):
    """Logout
    this api is responsible for Logout to user
    body:
        {
            "email": str,
            "password": str
        }
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        try:
            data["username"] = data["email"]
            logout(request)
            logging.info("logout success")
            return Response(
                data={"IsStatus": True, "Message": "User logout successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logging.error("logout faild because : " + str(e))
            return Response(
                data={"IsStatus": False, "Message": "logout failed try again."},
                status=status.HTTP_404_NOT_FOUND,
            )          
        