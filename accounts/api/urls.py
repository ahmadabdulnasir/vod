from django.urls import path

from .views import (
    ChangePassword,
    CreateAccountAPIView,
    CustomObtainAuthToken,
    ProfileCreateAPIView,
    UsersProfileListAPIView,
    ProfileDetailsAPIView,
    ProfileUpdateAPIView,
    UpdateAccountToMarchantAPIView,
    MarchantListAPIView,
    BranchListAPIView,
    SubscriptionPlanListAPIView,
    
)

# from .authentication.views import CustomObtainAuthToken, ChangePassword
urlpatterns = [
    path("jwt/", CustomObtainAuthToken.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("create-user/", CreateAccountAPIView.as_view()),
    path("create/profile/", ProfileCreateAPIView.as_view()),
    path("list/profile/", UsersProfileListAPIView.as_view()),
    path("profile/details/<pk>/", ProfileDetailsAPIView.as_view()),
    path("profile/update/<pk>/", ProfileUpdateAPIView.as_view()),
    path("profile/upgrade-to-marchant/", UpdateAccountToMarchantAPIView.as_view()),
    path("marchant/list/", MarchantListAPIView.as_view()),
    path("branch/list/", BranchListAPIView.as_view()),
    path("subscription-plan/list/", SubscriptionPlanListAPIView.as_view()),
]
