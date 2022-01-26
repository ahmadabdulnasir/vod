from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import View
from core.location.models import LGA, State
from accounts.models import  UserProfile, Marchant, Store
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from vod.models import (
    Category,
    Comment,
    Genre,
    Movie,
    MoviePoster,
    Review,
    Series,
    SeriesEpisode,
    Promotion
)

from .serializers import (
    CategorySerializer,
    CommentModelSerializer,
    GenreSerializer,
    MovieDetailsSerializer,
    MovieListSerializer,
    MoviePosterSerializer,
    ReviewModelSerializer,
    SeriesDetailsSerializer,
    SeriesListSerializer,
    # SeriesSeasonSerializer,
    # SeasonEpisodeSerializer,
    SeriesEpisodeDetailsSerializer,
    SeriesEpisodeListSerializer,
    PromotionSerializer,
     
)


from core.permissions.api_permissions import HasActiveCompany

from core.api.pagination import CorePagination


common_movie_series_keys = [
    "pk",
    "title",
    "uid",
    # "thumb",
    "get_thumb_url",
    "description",
    "get_genres",
    # "category",
    "category_title",
    "status",
    "access_level",
    "get_data_type",
    "timestamp",
    "updated",
]

TARGET_CONTENT_TYPES = {
    "movie": Movie, 
    "series": Series,
    "episode": SeriesEpisode,
}


class CategoryCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Category
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Save Success",
                "data": serializer.data,
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save()

class CategoryListAPIView(generics.ListAPIView):
    """
       List All Categories
    """
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Category.objects.all()
            status_ = self.request.GET.get("status")
            if status_:
                qs = qs.filter(status=status_)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

class CategoryDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of Category
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    lookup_field = "pk"

class CategoryUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Category
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    lookup_field = "pk"

class CategoryDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Category
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Category {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


class CategoryHomePageAPIView(APIView):
    """
       Return Category with series and movies list for Homepage
    """
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def get(self, request, format="json"):
        try:
            active_categories = Category.objects.filter(status=True).order_by("-updated")
            dta = [
                cat.get_form_format() for cat in active_categories
            ]
            status_code = status.HTTP_200_OK
            return Response(data=dta, status=status_code)
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )


class GenreCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Genre
    """
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Save Success",
                "data": serializer.data,
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save()

class GenreListAPIView(generics.ListAPIView):
    """
        List all Genre
    """
    serializer_class = GenreSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()

class GenreDetailsAPIView(generics.RetrieveAPIView):
    """
        Return Details of Genre
    """
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()
    lookup_field = "pk"

class GenreUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Genre
    """
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()
    lookup_field = "pk"

class GenreDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Genre
    """
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Genre {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

### Movie

class MovieCreateAPIView(generics.CreateAPIView):
    """
        Allows Upload of a Movie
    """
    serializer_class = MovieDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def create(self, request, *args, **kwargs):
        data = request.data #.copy()
        # print(type(data))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Adding genres
        # spam = serializer.instance
        # genres_pks = request.data.get("genres", "0").split(',')
        # print(genres_pks)
        # try:
        #     genres_pks = list(map(int, genres_pks))
        # except Exception as exp:
        #     # Delete the instance, because we have save it above befor adding genres
        #     # spam.delete()
        #     return Response(
        #         data={
        #             "detail": f"Invalid Selections of Genres. Error: {exp}",
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # if len(genres_pks) > 0:
        #     genres = Genre.objects.filter(pk__in=genres_pks)
        #     # print(genres)
        #     # data.update({"genres":genres})
        #     # spam.genres.add(*genres)
        # else:
        #     genres = []
        # spam.save()
        # self.perform_create(serializer, genres)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        dta = {
            "detail": "Movie Upload Success",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer, genres):
    def perform_create(self, serializer):
        return serializer.save(
            uploaded_by=self.request.user.profile,
            company=self.request.user.profile.company,
            # genres=genres
        )


# class MovieCreateAPIView(APIView):
#     """
#         Allows Upload of a Movie
#     """
#     serializer_class = MovieDetailsSerializer
#     permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

#     def post(self, request, format="json"):
#         print(request.data)
#         title = request.data.get("title")
#         thumb = request.data.get("thumb")
#         description = request.data.get("description")
#         #genres = request.data.get("genres")
#         category_pk = request.data.get("category_pk")
#         posters = request.data.get("posters")
#         video = request.data.get("video")
#         movie_status = request.data.get("status")
#         company_pk = request.data.get("company_pk")
#         error_list = []
#         required_info = {
#             # "profile_pk": profile_pk,
#             "title": title,
#             "thumb": thumb,
#             "description": description,
#             # "genres": genres,
#             # "category": category_pk,
#             # "posters": posters,
#             "video": video,
#             "movie_status": movie_status,
#             # "company_pk": company_pk,
#             "uploaded_by": request.user.profile,
#         }
#         for entry in required_info.keys():
#             if not required_info.get(entry):
#                 error_list.append(f"Invalid Entry of: {entry}")
#         if error_list:
#             dta = {
#                 "detail": "Fail to Upload Movie, None or Partial Data Received.",
#                 "errors": error_list,
#             }
#             status_code = 406
#             raise ValidationError(dta, code=status_code)
#         data = request.data #.copy()
#         try:
#             category = Category.objects.get(pk=category_pk)
#         except Category.DoesNotExist as exp:
#             category = None
#         #if isinstance(genres, list):
#         #    print("hh")
#         #    #genres_to_add = Genre.objects.filter(pk__in=genres)
#         #else:
#         #    genres_to_add = None
#         if isinstance(posters, list):
#             posters_to_add = []
#             for p in posters:
#                 spam = MoviePoster(
#                     title = p.get("title"),
#                     image = p.get("image"),
#                 )
#                 posters_to_add.append(spam)
#         else:
#             posters_to_add = None
#         try:
#             company = Marchant.objects.get(pk=company_pk)
#         except Marchant.DoesNotExist as exp:
#             # company = None
#             company = request.user.profile.company

#         # modifying Data
#         data["company"] = company
#         data["category"] = category
#         #if genres_to_add:
#         #    #data["genres"] = genres_to_add
#         #    pass
#         if posters_to_add:
#             data["posters"] = posters_to_add

#         try:
#             # serializer = self.get_serializer(data=request.data)
#             serializer = self.serializer_class(data=data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             # 
#             headers = self.get_success_headers(serializer.data)
#             dta = {
#                 "detail": "Movie Upload Success",
#                 "data": serializer.data
#             }
#             return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
#         except Exception as exp:
#             raise ValidationError({"detail": f"{exp}"})


class MovieListAPIView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Movie.objects.all()
            status_ = self.request.GET.get("status")
            for_user = self.request.GET.get("for_user")
            for_company = self.request.GET.get("for_company")
            access_level = self.request.GET.get("access_level")
            suggested = self.request.GET.get("suggested")
            latest = self.request.GET.get("latest")
            category = self.request.GET.get("category")
            music_only = self.request.GET.get("music_only")
            movies_only = self.request.GET.get("movies_only")
            genre_pk = self.request.GET.get("genre")
            if status_:
                qs = qs.filter(status=status_)
            if for_user and for_user == 'yes' and user.is_authenticated:
                qs = qs.filter(uploaded_by=user.profile)
            if for_company:
                qs = qs.filter(company=for_company)
            if access_level:
                qs = qs.filter(access_level=access_level)
            if suggested and suggested == "yes" and user.is_authenticated:
                pass
                # qs = qs.filter(access_level=access_level)
            if latest and latest == "yes":
                qs = qs.order_by("-timestamp")
            if category:
                qs = qs.filter(category=category)
            if music_only and music_only=="yes":
                qs = qs.filter(category__title__icontains="music")
            if movies_only and movies_only == "yes":
                #qs = qs.filter(category__title__icontains="movie")
                qs = qs.exclude(category__title__icontains="music")
            if genre_pk:
                qs = qs.filter(genres__in=[genre_pk])
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class MovieSearchAPIView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Movie.objects.all()
            active = self.request.GET.get("active")
            lga_pk = self.request.GET.get("lga_pk")
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class MovieDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Movie
    """
    serializer_class = MovieDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Movie.objects.all()
    lookup_field = "pk"


class MovieUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of Movie.
    """
    serializer_class = MovieDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Movie.objects.all()
    lookup_field = "pk"


class MovieDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Movie
    """
    serializer_class = MovieDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Movie.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Movie {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

### ./Movie

### Series

class SeriesCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Series
    """
    serializer_class = SeriesDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def create(self, request, *args, **kwargs):
        data = request.data  # .copy()
        # _p = data.pop("genres")
        # Adding genres
        genres_pks = request.data.get("genres", "0").split(',')
        try:
            genres_pks = list(map(int, genres_pks))
        except Exception as exp:
            return Response(
                data={
                    "detail": f"Invalid Selections of Genres. Error: {exp}",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(genres_pks) > 0:
            genres = Genre.objects.filter(pk__in=genres_pks)
        else:
            genres = []
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # spam.save()
        self.perform_create(serializer, genres)
        headers = self.get_success_headers(serializer.data)
        dta = {
            "detail": "Series Created Successfuly",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer, genres):
        return serializer.save(
            created_by=self.request.user.profile,
            company=self.request.user.profile.company,
            genres=genres
        )

class SeriesListAPIView(generics.ListAPIView):
    """
        List all Series
    """
    serializer_class = SeriesListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # queryset = Series.objects.all()
    pagination_class = CorePagination
    
    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Series.objects.all()
            status_ = self.request.GET.get("status")
            for_user = self.request.GET.get("for_user")
            for_company = self.request.GET.get("for_company")
            access_level = self.request.GET.get("access_level")
            suggested = self.request.GET.get("suggested")
            latest = self.request.GET.get("latest")
            category = self.request.GET.get("category")
            music_only = self.request.GET.get("music_only")
            movies_only = self.request.GET.get("movies_only")
            genre_pk = self.request.GET.get("genre")
            if status_:
                qs = qs.filter(status=status_)
            if for_user and for_user == 'yes' and user.is_authenticated:
                # print("for user checked")
                qs = qs.filter(created_by=user.profile)
                # print(qs)
            if for_company:
                qs = qs.filter(company=for_company)
            if access_level:
                qs = qs.filter(access_level=access_level)
            if suggested and suggested == "yes" and user.is_authenticated:
                pass
                # qs = qs.filter(access_level=access_level)
            if latest and latest == "yes":
                qs = qs.order_by("-timestamp")
            if category:
                qs = qs.filter(category=category)
            if music_only and music_only=="yes":
                qs = qs.filter(category__title__icontains="music")
            if movies_only and movies_only == "yes":
                qs = qs.filter(category__title__icontains="movie")
            if genre_pk:
                qs = qs.filter(genres__in=[genre_pk])
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class SeriesDetailsAPIView(generics.RetrieveAPIView):
    """
        Return Details of Series
    """
    serializer_class = SeriesDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Series.objects.all()
    lookup_field = "pk"


class SeriesUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Series
    """
    serializer_class = SeriesDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Series.objects.all()
    lookup_field = "pk"
    
    def perform_update(self, serializer):
        serializer.save()

class SeriesDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Series
    """
    serializer_class = SeriesDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Series.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Series {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

### ./Series


### Series Episode

class SeriesEpisodeCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Series Episode
    """
    serializer_class = SeriesEpisodeDetailsSerializer

    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # spam.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        dta = {
            "detail": "Series Episode Created Successfuly",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(
            uploaded_by=self.request.user.profile,
            company=self.request.user.profile.company,
        )


class SeriesEpisodeListAPIView(generics.ListAPIView):
    """
        List all Series Episode
    """
    serializer_class = SeriesEpisodeListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = SeriesEpisode.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = SeriesEpisode.objects.all()
            status_ = self.request.GET.get("status")
            series = self.request.GET.get("series")
            for_user = self.request.GET.get("for_user")
            if status_:
                qs = qs.filter(status=status_)
            if series:
                qs = qs.filter(series=series)
            if for_user and for_user == "yes" and user.is_authenticated:
                qs = qs.filter(uploaded_by=user.profile)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class SeriesEpisodeDetailsAPIView(generics.RetrieveAPIView):
    """
        Return Details of Series Episode
    """
    serializer_class = SeriesEpisodeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeriesEpisode.objects.all()
    lookup_field = "pk"


class SeriesEpisodeUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Series Episode
    """
    serializer_class = SeriesEpisodeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeriesEpisode.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


class SeriesEpisodeDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Series Episode
    """
    serializer_class = SeriesEpisodeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeriesEpisode.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Series Episode: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

### ./Series Episode
### Movie - Series Common

class MoviesSeriesSearchAPIView(APIView):
    """API to search Movies and Series and return Combined Result

    Args:
        APIView (search_query): Search Query Term

    Raises:
        APIException: [description]

    Returns:
        [dict]: [Details of Search and Combined Movies and Series based on the Search Term list based on common keys between the two]
    """
    serializer_class = MovieListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get(self, request, format="json"):
        try:
            movies_qs = Movie.objects.filter(status="published").order_by("-timestamp")
            series_qs = Series.objects.filter(status="published").order_by("-timestamp")
            search_query = self.request.GET.get("search_query")
            movies_qs_combo = movies_qs.filter(
                title__icontains=search_query) | movies_qs.filter(description__icontains=search_query
                )
            series_qs_combo = series_qs.filter(
                title__icontains=search_query) | series_qs.filter(description__icontains=search_query
                )
            # print(series_qs_combo)
            # complete_qs = movies_qs_combo | series_qs_combo
            complete_qs = list(movies_qs_combo[:50]) + list(series_qs_combo[:50] )

            egg = []
            for item in complete_qs:
                spam = {c_k: getattr(item, c_k) for c_k in common_movie_series_keys}
                egg.append(spam)
            status_code = status.HTTP_200_OK
            dta = {
                "detail": f"Search Result of: {search_query}",
                "data": egg
            }
            return Response(dta, status=status_code)
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )


class CommentCreateAPIView(APIView):
    """API to add Comment to Movies and Series
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format="json"):
        content_pk = self.request.POST.get("content_pk")
        target_content = self.request.POST.get("target_content")
        comment = self.request.POST.get("comment")
        user = request.user
        error_list = []
        required_info = {
            "content_pk": content_pk,
            "target_content": target_content,
            "comment": comment,
            # "uploaded_by": request.user.profile,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Add Comment, None or Partial Data Received.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)
        if target_content not in ["movie", "series", "seriesepisode"]:
            dta = {
                "detail": "Invalid Target Content Type",
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)

        try:
            # content_type_target = TARGET_CONTENT_TYPES.get(target_content)
            # print(target_content)
            content_type = ContentType.objects.get(app_label='vod', model=target_content)
            # print(content_type)
            comment = Comment(
                content_type=content_type,
                object_id=content_pk,
                author=user.profile,
                body=comment,
                status="review"
            )
            comment.save()
            comment_serializer = CommentModelSerializer(instance=comment, context={'request': request})
            status_code = status.HTTP_200_OK
            dta = {
                "detail": f"Comment Added Successfully",
                "data": comment_serializer.data
            }
            return Response(dta, status=status_code)
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )


class CommentListAPIView(generics.ListAPIView):
    """
        List all Comments based on Query Params
    """
    serializer_class = CommentModelSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Comment.objects.all()
            status_ = self.request.GET.get("status")
            for_user = self.request.GET.get("for_user")
            content_pk = self.request.GET.get("content_pk")
            target_content = self.request.GET.get("target_content")
            # print(content_pk)
            # print(target_content)
            allowed_target_content =  ["movie", "series", "seriesepisode"]
            if status_:
                qs = qs.filter(status=status_)
            if for_user and for_user == 'yes' and user.is_authenticated:
                qs = qs.filter(author=user.profile)
            if content_pk and target_content and target_content in allowed_target_content:
                target_content_type = ContentType.objects.get(app_label='vod', model=target_content)
                # print(target_content_type)
                qs = qs.filter(content_type=target_content_type, object_id=content_pk)
            if target_content and target_content not in allowed_target_content:
                raise APIException(
                    detail=f"Unknown target_content: {target_content}", code=status.HTTP_417_EXPECTATION_FAILED
                )
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class CommentUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Comment
    """
    serializer_class = CommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


class CommentDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Comment
    """
    serializer_class = CommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Comment: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


class ReviewCreateAPIView(APIView):
    """API to add Review to Movies and Series
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format="json"):
        content_pk = self.request.POST.get("content_pk")
        target_content = self.request.POST.get("target_content")
        review = self.request.POST.get("review")
        rate = self.request.POST.get("rate")
        user = request.user
        error_list = []
        required_info = {
            "content_pk": content_pk,
            "target_content": target_content,
            "review": review,
            "rate": rate,
            # "uploaded_by": request.user.profile,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Add Review, None or Partial Data Received.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)
        if target_content not in ["movie", "series", "seriesepisode"]:
            dta = {
                "detail": "Invalid Target Content Type",
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)

        try:
            # content_type_target = TARGET_CONTENT_TYPES.get(target_content)
            # print(target_content)
            content_type = ContentType.objects.get(app_label='vod', model=target_content)
            # print(content_type)
            comment = Review(
                content_type=content_type,
                object_id=content_pk,
                author=user.profile,
                body=review,
                rate=rate,
                status="review"
            )
            comment.save()
            comment_serializer = ReviewModelSerializer(instance=comment, context={'request': request})
            status_code = status.HTTP_200_OK
            dta = {
                "detail": f"Review Added Successfully",
                "data": comment_serializer.data
            }
            return Response(dta, status=status_code)
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )


class ReviewListAPIView(generics.ListAPIView):
    """
        List all Reviews based on Query Params
    """
    serializer_class = ReviewModelSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Review.objects.all()
            status_ = self.request.GET.get("status")
            for_user = self.request.GET.get("for_user")
            content_pk = self.request.GET.get("content_pk")
            target_content = self.request.GET.get("target_content")
            allowed_target_content = ["movie", "series", "seriesepisode"]
            if status_:
                qs = qs.filter(status=status_)
            if for_user and for_user == 'yes' and user.is_authenticated:
                qs = qs.filter(author=user.profile)
            if content_pk and target_content and target_content in allowed_target_content:
                target_content_type = ContentType.objects.get(app_label='vod', model=target_content)
                qs = qs.filter(content_type=target_content_type, object_id=content_pk)
            if target_content and target_content not in allowed_target_content:
                raise APIException(
                    detail=f"Unknown target_content: {target_content}", code=status.HTTP_417_EXPECTATION_FAILED
                )
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Review
    """
    serializer_class = ReviewModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


class ReviewDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Review
    """
    serializer_class = ReviewModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Review: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)



### ./Movie - Series Common

## ADS | Promotions

class PromotionCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Promotion
    """
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Save Success",
                "data": serializer.data,
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save()


class PromotionListAPIView(generics.ListAPIView):
    """
        List all Promotion
    """
    serializer_class = PromotionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # queryset = Promotion.objects.all()
    def get_queryset(self, *args, **kwargs):
        try:
            qs = Promotion.objects.all()
            active = self.request.GET.get("active")
            location = self.request.GET.get("location")
            type_ = self.request.GET.get("type")
            status_code = status.HTTP_200_OK
            if location and location in [ "main_home_slider", "home_slider", "breadcrumb_slider", "login_page" ]:
                qs = qs.filter(location=location)
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if type_:
                qs = qs.filter(type=type_)
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class PromotionDetailsAPIView(generics.RetrieveAPIView):
    """
        Return Details of Promotion
    """
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Promotion.objects.all()
    lookup_field = "pk"


class PromotionUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Promotion
    """
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Promotion.objects.all()
    lookup_field = "pk"


class PromotionDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Promotion
    """
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Promotion.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Promotion {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
## ./ADS | Promotions

## Dashboard


class GeneralDashboard(APIView):
    """
        General Dashboard Statistics
    """
    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def get(self, request, format="json"):
        import random 
        
        user = request.user
        profile = user.profile
        all_movies = Movie.objects.all()
        all_series = Series.objects.all()
        total_subscribers_users = UserProfile.objects.filter(plan__isnull=False)
        total_subscribers_marchant = UserProfile.objects.filter(plan__isnull=False)
        total_subscribers = total_subscribers_users.count() + total_subscribers_marchant.count()
        total_revenue = 644673.73
        # total_revenue = UserProfile.objects.filter(subscribtion_date__gt=today)
        top_marchants = Marchant.objects.all().values_list("title", flat=True)
        top_rated_items_movies = list(all_movies[:2]) #.values(*common_keys)
        top_rated_items_series = list(all_series[:2]) #.values(*common_keys)
        top_rated_items = top_rated_items_movies + top_rated_items_series
        # print(all_movies[:2])
        random.shuffle(top_rated_items)
        top_rated_items_data = []
        for item in top_rated_items:
            spam = { c_k:getattr(item,c_k) for c_k in common_movie_series_keys }
            top_rated_items_data.append(spam)
        # top_rated_items
        # print(top_rated_items_data)
        try:
            dta = {
                "total_movies": all_movies.count(),
                "total_series": all_series.count(),
                "subscribers": f"{total_subscribers:,.2f}",
                "total_revenue": f"₦{total_revenue:,.2f}",
                "top_marchants": top_marchants,
                "top_rated_items": top_rated_items_data,
            }
            return Response(data=dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"{exp}"})


class MarchantDashboard(APIView):
    """
        Marchant Dashboard Statistics
    """
    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def get(self, request, format="json"):
        user = request.user
        profile = user.profile
        company = profile.company
        all_movies = Movie.objects.filter(company=company)
        all_series = Series.objects.filter(company=company)
        total_subscribers = -999
        total_revenue = 644673.73
        try:
            dta = {
                "total_movies": all_movies.count(),
                "total_series": all_series.count(),
                "subscribers": f"{total_subscribers:,.2f}",
                "total_revenue": f"₦{total_revenue:,.2f}"
            }
            return Response(data=dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"{exp}"})
## ./Dashboard
