from core.api.serializers import CustomeSerializer
from vod.models import (
    Category, 
    Genre, 
    Movie,
    MoviePoster,
    Review,
    Series, 
    # SeriesSeason,
    # SeasonEpisode, 
    SeriesEpisode,
    Comment,
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
    # genres = GenreSerializer(many=True)

    # def get_or_update_genres(self, genres):
    #         package_ids = []
    #         # for package in packages:
    #         #     # package_instance, created = Genre.objects.update_or_create(pk=package.get('id'), defaults=package)
    #         #     package_instance, created = Genre.objects.update_or_create(pk=package.get('pk'), defaults=package)
    #         #     package_ids.append(package_instance.pk)
    #         # return package_ids
    #         genres_pk = [genre.get("pk") for genre in genres]
    #         spam = Genre.objects.filter(pk__in=genres_pk)
    #         return spam


    # def update(self, instance, validated_data):
    #     # genres = validated_data.pop('genres', [])
    #     genres = validated_data.pop('genres_pk', [])
    #     print(genres)
    #     instance.genres.set(self.get_or_update_genres(genres))
    #     # fields = ['order_id', 'is_cod']
    #     # for field in fields:
    #     #     try:
    #     #         setattr(instance, field, validated_data[field])
    #     #     except KeyError:  # validated_data may not contain all fields during HTTP PATCH
    #     #         pass
    #     # try:
    #     print("Update Movie")

    #     instance.save()
    #     return instance
        
    class Meta:
        model = Movie
        fields = [
            "pk", 
            "title",
            "uid",
            "thumb",
            "description",
            "release_year",
            "running_time",
            "genres",
            "get_genres",
            "get_posters",
            "category",
            "category_title",
            "video",
            "video_link",
            "get_rating",
            "status",
            "access_level",
            "get_related",
            # "uploaded_by",
            "get_data_type",
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
            "release_year",
            "running_time",
            "genres",
            "get_genres",
            "category",
            "category_title",
            # "posters",
            # "video",
            "get_rating",
            "status",
            "access_level",
            "get_data_type",
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
            "release_year",
            "running_time",
            "genres",
            "get_genres",
            "category",
            "category_title",
            "get_rating",
            "status",
            "access_level",
            "number_of_episodes",
            "get_episodes",
            "get_related",
            "get_data_type",
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
            "release_year",
            "running_time",
            "genres",
            "get_genres",
            "category",
            "category_title",
            "get_rating",
            "status",
            "access_level",
            "number_of_episodes",
            "get_data_type",
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
            "get_rating",
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


class MovieSeriesListSerializer(CustomeSerializer):

    class Meta:
        model = Movie
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
            # "posters",
            # "video",
            "status",
            "access_level",
            "get_data_type",
            "timestamp",
            "updated",
        ]


class CommentModelSerializer(CustomeSerializer):

    class Meta:
        model = Comment
        fields = [
            "pk",
            "content_type",
            "object_id",
            # "content_object",
            "object_repr",
            "get_data_type",
            "author",
            "author_title",
            "body",
            "status",
            "timestamp",
            "updated",
        ]


class ReviewModelSerializer(CustomeSerializer):

    class Meta:
        model = Review
        fields = [
            "pk",
            "content_type",
            "object_id",
            # "content_object",
            "object_repr",
            "get_data_type",
            "author",
            "author_title",
            "body",
            "rate",
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
            "get_obj_access_level",
            "active",
            "timestamp", 
            "updated",
            ]
