from core.api.serializers import CustomeSerializer
from vod.models import Category, Genre, Movie, MoviePoster, Series, SeriesSeason, SeasonEpisode
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MovieSerializer(CustomeSerializer):

    class Meta:
        model = Movie
        fields = [
            "pk", 
            "title",
            "uid",
            "thumb",
            "description",
            "get_genres",
            "get_posters",
            "category",
            "video",
            "video_link",
            "status",
            "access_level",
            "category_title",
            # "uploaded_by",
            "timestamp", 
            "updated",
            ]
        # read_only_fields = ["uploaded_by",]


class MovieListSerializer(CustomeSerializer):

    class Meta:
        model = Movie
        fields = [
            "pk",
            "title",
            "uid",
            "thumb",
            "description",
            "get_genres",
            "category",
            "category_title",
            # "posters",
            "video",
            "status",
            "access_level",
            "timestamp",
            "updated",
            ]


class CategorySerializer(CustomeSerializer):

    class Meta:
        model = Category
        fields = [
            "pk",
            "title",
            "timestamp",
            "updated",
        ]


class GenreSerializer(CustomeSerializer):

    class Meta:
        model = Genre
        fields = [
            "pk", 
            "title",
            "timestamp", 
            "updated",
            ]


class MoviePosterSerializer(CustomeSerializer):

    class Meta:
        model = MoviePoster
        fields = [
            "pk", 
            "title",
            "timestamp", 
            "updated",
            ]


class SeriesSerializer(CustomeSerializer):

    class Meta:
        model = Series
        fields = [
            "pk", 
            "title",
            "timestamp", 
            "updated",
            ]


class SeriesSeasonSerializer(CustomeSerializer):

    class Meta:
        model = SeriesSeason
        fields = [
            "pk", 
            "title",
            "timestamp", 
            "updated",
            ]


class SeasonEpisodeSerializer(CustomeSerializer):

    class Meta:
        model = SeasonEpisode
        fields = [
            "pk", 
            "title",
            "timestamp", 
            "updated",
            ]


