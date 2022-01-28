from django.urls import path

from .views import (
    MainPageCreateAPIView,
    MainPageListAPIView,
    MainPageDetailsAPIView,
    MainPageUpdateAPIView,
    MainPageDeleteAPIView,
    SiteInformationCreateAPIView,
    SiteInformationListAPIView,
    SiteInformationDetailsAPIView,
    SiteInformationUpdateAPIView,
    SiteInformationDeleteAPIView,
    )

urlpatterns = [
    path("main-page/create/", MainPageCreateAPIView.as_view()),
    path("main-page/list/", MainPageListAPIView.as_view()),
    path("main-page/details/<slug>/", MainPageDetailsAPIView.as_view()),
    path("main-page/update/<slug>/", MainPageUpdateAPIView.as_view()),
    path("main-page/delete/<slug>/", MainPageDeleteAPIView.as_view()),

    path("site-information/create/", SiteInformationCreateAPIView.as_view()),
    path("site-information/list/", SiteInformationListAPIView.as_view()),
    path("site-information/details/<slug>/", SiteInformationDetailsAPIView.as_view()),
    path("site-information/update/<slug>/", SiteInformationUpdateAPIView.as_view()),
    path("site-information/delete/<slug>/", SiteInformationDeleteAPIView.as_view()),
]
