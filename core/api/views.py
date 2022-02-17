from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import MainPage, SiteInformation

from .api_serializers import (
    MainPageDetailsSerializer,
    MainPageListSerializer,
    SiteInformationDetailsSerializer,
    SiteInformationListSerializer,

)


from core.permissions.api_permissions import HasActiveCompany

from core.api.pagination import CorePagination


class MainPageCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a MainPage
    """
    serializer_class = MainPageDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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


class MainPageListAPIView(generics.ListAPIView):
    """
       List All Categories
    """
    serializer_class = MainPageListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = MainPage.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = MainPage.objects.all()
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


class MainPageDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of MainPage
    """
    serializer_class = MainPageDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = MainPage.objects.all()
    lookup_field = "slug"


class MainPageUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating MainPage
    """
    serializer_class = MainPageDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = MainPage.objects.all()
    lookup_field = "slug"


class MainPageDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a MainPage
    """
    serializer_class = MainPageDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = MainPage.objects.all()
    lookup_field = "slug"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"MainPage {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


class SiteInformationCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a SiteInformation
    """
    serializer_class = SiteInformationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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


class SiteInformationListAPIView(generics.ListAPIView):
    """
       List All Categories
    """
    serializer_class = SiteInformationListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = SiteInformation.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = SiteInformation.objects.all()
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


class SiteInformationDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of SiteInformation
    """
    serializer_class = SiteInformationDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = SiteInformation.objects.all()
    lookup_field = "slug"


class SiteInformationUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating SiteInformation
    """
    serializer_class = SiteInformationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = SiteInformation.objects.all()
    lookup_field = "slug"


class SiteInformationDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a SiteInformation
    """
    serializer_class = SiteInformationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = SiteInformation.objects.all()
    lookup_field = "slug"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"SiteInformation {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
