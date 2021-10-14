from django.contrib.auth import models
from core.location.models import LGA, State
from accounts.models import  UserProfile, Marchant, Store
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from vod.models import Category, Genre
from .serializers import (
    MovieSerializer,
    MovieListSerializer,
    CategorySerializer,
    GenreSerializer,
    PosterSerializer,
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


class MovieCreateAPIView(APIView):
    """
        Allows Upload of a Movie
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated, HasActiveCompany]

    def post(self, request, format="json"):
        # survey_pk = request.data.get("survey_pk")
        # survey_pk = self.kwargs.get("pk")
        #survey_pk = pk
        title = request.data.get("title")
        thumb = request.data.get("thumb")
        description = request.data.get("description")
        genre = request.data.get("genre")
        category = request.data.get("category")
        posters = request.data.get("posters")
        video = request.data.get("video")
        movie_status = request.data.get("status")
        company_pk = request.data.get("company_pk")
        error_list = []
        required_info = {
            # "profile_pk": profile_pk,
            "title": title,
            "thumb": thumb,
            "description": description,
            # "genre": genre,
            "category": category,
            # "posters": posters,
            "video": video,
            "movie_status": movie_status,
            "company_pk": company_pk,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Upload Movie, Non or Partial Data Received.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # 
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Movie Upload Success",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"{exp}"})


class MovieListAPIView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            qs = UserProfile.objects.all()
            active = self.request.GET.get("active")
            lga_pk = self.request.GET.get("lga_pk")
            state = self.request.GET.get("state")
            user_type = self.request.GET.get("user_type")
            group_pk = self.request.GET.get("group_pk")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            if lga_pk:
                qs = qs.filter(lga=lga_pk)
            if state:
                qs = qs.filter(state=state)
            if user_type:
                qs = qs.filter(user_type=user_type)
            if group_pk:
                group = get_object_or_404(Group, pk=group_pk)
                group_users = group.user_set.all()
                qs = qs.filter(user__in=group_users)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class MovieSearchAPIView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            qs = UserProfile.objects.all()
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
    queryset = UserProfile.objects.all()
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



