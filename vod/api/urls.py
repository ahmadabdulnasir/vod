from django.urls import path

from .views import (CategoryListAPIView, GenreListAPIView, MovieCreateAPIView,
                    MovieDetailsAPIView, MovieListAPIView, MovieSearchAPIView,
                    MovieUpdateAPIView)

urlpatterns = [
    path("category/list/", CategoryListAPIView.as_view()),
    path("genre/list/", GenreListAPIView.as_view()),
    path("movie/create/", MovieCreateAPIView.as_view()),
    path("movie/list/", MovieListAPIView.as_view()),
    path("movie/search/", MovieSearchAPIView.as_view()),
    path("movie/details/<pk>/", MovieDetailsAPIView.as_view()),
    path("movie/update/<pk>/", MovieUpdateAPIView.as_view()),
    # path("marchant/list/", MarchantListAPIView.as_view()),
    # path("branch/list/", BranchListAPIView.as_view()),
]
