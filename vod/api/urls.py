from django.urls import path

from .views import (
    CategoryCreateAPIView,CategoryDetailsAPIView, CategoryUpdateAPIView, CategoryListAPIView, CategoryDeleteAPIView,
    GenreCreateAPIView, GenreDetailsAPIView, GenreUpdateAPIView, GenreListAPIView, GenreDeleteAPIView,
    MovieCreateAPIView, MovieDetailsAPIView, MovieListAPIView, 
    MovieSearchAPIView, MovieUpdateAPIView
    )

urlpatterns = [
    path("category/create/", CategoryCreateAPIView.as_view()),
    path("category/details/<pk>/", CategoryDetailsAPIView.as_view()),
    path("category/update/<pk>/", CategoryUpdateAPIView.as_view()),
    path("category/list/", CategoryListAPIView.as_view()),
    path("category/delete/<pk>/", CategoryDeleteAPIView.as_view()),
    path("genre/create/", GenreCreateAPIView.as_view()),
    path("genre/details/<pk>/", GenreDetailsAPIView.as_view()),
    path("genre/update/<pk>/", GenreUpdateAPIView.as_view()),
    path("genre/list/", GenreListAPIView.as_view()),
    path("genre/delete/<pk>/", GenreDeleteAPIView.as_view()),
    path("movie/create/", MovieCreateAPIView.as_view()),
    path("movie/list/", MovieListAPIView.as_view()),
    path("movie/search/", MovieSearchAPIView.as_view()),
    path("movie/details/<pk>/", MovieDetailsAPIView.as_view()),
    path("movie/update/<pk>/", MovieUpdateAPIView.as_view()),
    # path("marchant/list/", MarchantListAPIView.as_view()),
    # path("branch/list/", BranchListAPIView.as_view()),
]
