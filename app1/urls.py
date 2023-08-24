from django.urls import path
from . import views
from django.urls import include
# from rest_framework import routers                 
# router = routers.DefaultRouter()

urlpatterns = [
    # path('api-', include(router.urls)),
    path('user/register/', views.SignUp.as_view(), name="user-register"),
    path('user/login/', views.SignIn.as_view(), name="user-login"),
    path('user/logout/', views.Logout.as_view(), name="user-logout"),

]