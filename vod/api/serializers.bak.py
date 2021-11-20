from core.api.serializers import CustomeSerializer
from vod.models import (
    Category, 
    Genre, 
    Movie,
    MoviePoster,
    Series, 
    # SeriesSeason,
    # SeasonEpisode, 
    SeriesEpisode,
    Promotion
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CategorySerializer(CustomeSerializer):

    class Meta:
        model = Category
        fields = [
            "pk",
            "title",
            "description",
            "status",
            "timestamp",
            "updated",
        ]


class GenreSerializer(CustomeSerializer):

    class Meta:
        model = Genre
        fields = [
            "pk",
            "title",
            "description",
            "status",
            "timestamp",
            "updated",
        ]



class MovieDetailsSerializer(CustomeSerializer):
    # genres = GenreSerializer(read_only=False, many=True)
    #genres = GenreSerializer(many=True)
        
    class Meta:
        model = Movie
        fields = [
            "pk", 
            "title",
            "uid",
            "thumb",
            "description",
            #"genres",
            "get_genres",
            "get_posters",
            "category",
            "category_title",
            "video",
            "video_link",
            "status",
            "access_level",
            "get_related",
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
            # "video",
            "status",
            "access_level",
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


class SeriesDetailsSerializer(CustomeSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Series
        fields = [
            "pk",
            "title",
            "uid",
            "thumb",
            "description",
            "genres",
            "get_genres",
            "category",
            "category_title",
            "status",
            "access_level",
            "number_of_episodes",
            "get_episodes",
            "get_related",
            "timestamp",
            "updated",
        ]

class SeriesListSerializer(CustomeSerializer):

    class Meta:
        model = Series
        fields = [
            "pk", 
            "title",
            "uid",
            "thumb",
            "description",
            "genres",
            "get_genres",
            "category",
            "category_title",
            "status",
            "access_level",
            "number_of_episodes",
            "timestamp", 
            "updated",
            ]




# class SeriesSeasonSerializer(CustomeSerializer):

#     class Meta:
#         model = SeriesSeason
#         fields = [
#             "pk", 
#             "title",
#             "timestamp", 
#             "updated",
#             ]


# class SeasonEpisodeSerializer(CustomeSerializer):

#     class Meta:
#         model = SeasonEpisode
#         fields = [
#             "pk", 
#             "title",
#             "timestamp", 
#             "updated",
#             ]

class SeriesEpisodeDetailsSerializer(CustomeSerializer):

    class Meta:
        model = SeriesEpisode
        fields = [
            "pk", 
            "series",
            "series_title",
            "title",
            "uid",
            "thumb",
            "description",
            "video",
            "status",
            "timestamp", 
            "updated",
            ]


class SeriesEpisodeListSerializer(CustomeSerializer):

    class Meta:
        model = SeriesEpisode
        fields = [
            "pk",
            "series",
            "series_title",
            "title",
            "uid",
            "thumb",
            "description",
            "video",
            "status",
            "timestamp",
            "updated",
        ]


class PromotionSerializer(CustomeSerializer):

    class Meta:
        model = Promotion
        fields = [
            "pk",
            "uid",
            "title",
            "type",
            "object_id",
            "poster",
            "description",
            "location",
            "start_date",
            "end_date",
            "active",
            "timestamp", 
            "updated",
            ]
