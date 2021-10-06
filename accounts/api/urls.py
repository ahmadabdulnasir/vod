from django.urls import path

from .views import (
    ChangePassword,
    CreateAccountAPIView,
    CustomObtainAuthToken,
    ProfileCreateAPIView,
    ProfileDetailsAPIView,
    ProfileUpdateAPIView,
    UsersProfileListAPIView,
    MarchantListAPIView,
    BranchListAPIView,
    
)

# from .authentication.views import CustomObtainAuthToken, ChangePassword
urlpatterns = [
    path("jwt/", CustomObtainAuthToken.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("create-user/", CreateAccountAPIView.as_view()),
    path("create/profile/", ProfileCreateAPIView.as_view()),
    path("list/profile/", UsersProfileListAPIView.as_view()),
    path("details/profile/<pk>/", ProfileDetailsAPIView.as_view()),
    path("update/profile/<pk>/", ProfileUpdateAPIView.as_view()),
    path("marchant/list/", MarchantListAPIView.as_view()),
    path("branch/list/", BranchListAPIView.as_view()),
]
