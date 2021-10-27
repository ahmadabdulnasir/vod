from django.contrib.auth import models
from core.location.models import LGA, State
from accounts.models import  UserProfile, Marchant, Store
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from vod.models import Category, Genre, Movie, MoviePoster
from .serializers import (
    MovieSerializer,
    MovieListSerializer,
    CategorySerializer,
    GenreSerializer,
    MoviePosterSerializer,
    SeriesSerializer,
    SeriesSeasonSerializer,
    SeasonEpisodeSerializer,
     
)


from core.permissions.api_permissions import HasActiveCompany


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()


class GenreListAPIView(generics.ListAPIView):
    serializer_class = GenreSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()


class MovieCreateAPIView(generics.CreateAPIView):
    """
        Allows Upload of a Movie
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]


    def create(self, request, *args, **kwargs):
        data = request.data #.copy()
        # print(type(data))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Adding genres
        # spam = serializer.instance
        genres_pks = request.data.get("genres", "0").split(',')
        # print(genres_pks)
        try:
            genres_pks = list(map(int, genres_pks))
        except Exception as exp:
            # Delete the instance, because we have save it above befor adding genres
            # spam.delete()
            return Response(
                data={
                    "detail": f"Invalid Selections of Genres. Error: {exp}",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(genres_pks) > 0:
            genres = Genre.objects.filter(pk__in=genres_pks)
            # print(genres)
            # data.update({"genres":genres})
            # spam.genres.add(*genres)
        else:
            genres = []
        # spam.save()
        self.perform_create(serializer, genres)
        headers = self.get_success_headers(serializer.data)
        dta = {
            "detail": "Movie Upload Success",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, genres):
        return serializer.save(
            uploaded_by=self.request.user.profile,
            company=self.request.user.profile.company,
            genres=genres
        )


# class MovieCreateAPIView(APIView):
#     """
#         Allows Upload of a Movie
#     """
#     serializer_class = MovieSerializer
#     permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

#     def post(self, request, format="json"):
#         title = request.data.get("title")
#         thumb = request.data.get("thumb")
#         description = request.data.get("description")
#         genres = request.data.get("genres")
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
#             "category": category_pk,
#             # "posters": posters,
#             "video": video,
#             "movie_status": movie_status,
#             "company_pk": company_pk,
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
#         data = request.data.copy()
#         try:
#             category = Category.objects.get(pk=category_pk)
#         except Category.DoesNotExist as exp:
#             category = None
#         if isinstance(genres, list):
#             genres_to_add = Genre.objects.filter(pk__in=genres)
#         else:
#             genres_to_add = None
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
#             company = None

#         # modifying Data
#         data["company"] = company
#         data["category"] = category
#         if genres_to_add:
#             data["genres"] = genres_to_add
#         if posters_to_add:
#             data["posters"] = posters_to_add

#         try:
#             # serializer = self.get_serializer(data=request.data)
#             serializer = self.get_serializer(data=data)
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

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = Movie.objects.all()
            status_ = self.request.GET.get("status")
            for_user = self.request.GET.get("for_user")
            for_company = self.request.GET.get("for_company")
            access_level = self.request.GET.get("access_level")
            suggested = self.request.GET.get("suggested")
            if status_:
                qs = qs.filter(status=status_)
            if for_user and for_user == 'yes' and user.is_authenticated:
                qs = qs.filter(uploaded_by=user.profile)
            if for_company:
                qs = qs.filter(company=for_company)
            if access_level:
                qs = qs.filter(access_level=access_level)
            if suggested and suggested == "yes":
                pass
                # qs = qs.filter(access_level=access_level)
           
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
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Movie.objects.all()
    lookup_field = "pk"


class MovieUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of Movie.
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [MyGenericViewset]
    queryset = UserProfile.objects.all()
    lookup_field = "pk"



