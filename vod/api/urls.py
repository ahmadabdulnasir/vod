from django.urls import path

from .views import (
    CategoryCreateAPIView, CategoryListAPIView, CategoryDetailsAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView,
    GenreCreateAPIView, GenreListAPIView, GenreDetailsAPIView, GenreUpdateAPIView, GenreDeleteAPIView,
    MovieCreateAPIView, MovieDetailsAPIView, MovieListAPIView, 
    MovieSearchAPIView, MovieUpdateAPIView,
    PromotionCreateAPIView, PromotionListAPIView, PromotionDetailsAPIView, PromotionUpdateAPIView, PromotionDeleteAPIView,
    )

urlpatterns = [
    path("category/create/", CategoryCreateAPIView.as_view()),
    path("category/list/", CategoryListAPIView.as_view()),
    path("category/details/<pk>/", CategoryDetailsAPIView.as_view()),
    path("category/update/<pk>/", CategoryUpdateAPIView.as_view()),
    path("category/delete/<pk>/", CategoryDeleteAPIView.as_view()),
    path("genre/create/", GenreCreateAPIView.as_view()),
    path("genre/list/", GenreListAPIView.as_view()),
    path("genre/details/<pk>/", GenreDetailsAPIView.as_view()),
    path("genre/update/<pk>/", GenreUpdateAPIView.as_view()),
    path("genre/delete/<pk>/", GenreDeleteAPIView.as_view()),
    path("movie/create/", MovieCreateAPIView.as_view()),
    path("movie/list/", MovieListAPIView.as_view()),
    path("movie/search/", MovieSearchAPIView.as_view()),
    path("movie/details/<pk>/", MovieDetailsAPIView.as_view()),
    path("movie/update/<pk>/", MovieUpdateAPIView.as_view()),
    # path("marchant/list/", MarchantListAPIView.as_view()),
    # path("branch/list/", BranchListAPIView.as_view()),
    path("promotion/create/", PromotionCreateAPIView.as_view()),
    path("promotion/list/", PromotionListAPIView.as_view()),
    path("promotion/details/<pk>/", PromotionDetailsAPIView.as_view()),
    path("promotion/update/<pk>/", PromotionUpdateAPIView.as_view()),
    path("promotion/delete/<pk>/", PromotionDeleteAPIView.as_view()),
]
