from core.location.models import LGA, State
from accounts.models import  UserProfile, Marchant, Store
from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from .serializers import (
    MarchantSerializer,
    StoreSerializer,
    UserProfileListSerializer,
    UserProfileSerializer, 
)

User = get_user_model()

class CreateAccountAPIView(APIView):
    def post(self, request, format=None):
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        # user_profile
        phone_number = request.POST.get("phone_number")
        dob = request.POST.get("dob")
        state_pk = request.POST.get("state")
        lga_pk = request.POST.get("lga")
        address = request.POST.get("address")
        user_type = request.POST.get("user_type")
        image = request.FILES.get("image")
        if (
            not username
            or not password
            or not first_name
            or not last_name
            or not image
            or not email
            or not phone_number
            or not dob
            or not state_pk
            or not lga_pk
            or not address
            or not user_type
        ):
            dta = {
                "detail": """Fail to Create user, Non or Partial Data Received.
                Please Provide all of: `username`, `password`, `first_name`, 
                `last_name`, `email`, `phone_number`, `dob`, `state|lga`, `address`,
                `group_pk`, `designation_pk`, `branch_pk`, `user_type`!!"""
            }
            status_code = 406
            raise ValidationError(dta, status_code)
        else:
            try:
                # create user
                if username.count(' ')>0:
                    return Response(data={"detail": "Username Cannot contain space"}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create(username=username)
            except IntegrityError as exp:
                raise ValidationError({"detail": f"{username} Already Exist Error: {exp}"})
            
            #  check for duplicate email
            user_with_email = User.objects.filter(email=email)
            if user_with_email.count() > 0:
                raise ValidationError({"detail": f"User with email: {email} Already Exist!"})
            
            # check for state and lga validity
            lga = None
            state = None
            try:
                lga = get_object_or_404(LGA, pk=lga_pk)
                state = get_object_or_404(State,pk=state_pk)
            except Exception as exp:
                raise ValidationError({"detail": "Invalid Entry for State and/or LGA."})
            
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # valid designation and branch
            
            try:
                egg = {
                    "user": user,
                    "user_type": user_type,
                    "image": image if image else None,
                    "surname": last_name,
                    "other_names": first_name,
                    "phone_number": phone_number,
                    "email": email,
                    "dob": dob,
                    "state": state,
                    "lga": lga,
                    "address": address,
                }
                profile = UserProfile(**egg)               
                profile.save()
            except Exception as exp:
                # Delete The Created User
                user.delete()
                msg = f"Error while creating profile for the user: {username}"
                raise ValidationError(
                    {"detail": f"Validation Error while creating profile: {exp}", "message": msg}
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                profile = user.profile
                profile_serializer = UserProfileSerializer(profile, context={'request': request})
                dta = {
                    "message": "User Created Successfully.",
                    "token": f"{token}",
                    "profile": profile_serializer.data,
                }
                status_code = 201
        return Response(dta, status=status_code)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                # user_serializer = UserSerializer(user)
                profile = user.profile
                profile_serializer = UserProfileSerializer(profile, context={'request': request})
                data = {
                    "token": token.key,
                    # "user": user_serializer.data,
                    "profile": profile_serializer.data,
                }
            else:
                data = {"detail": "Invalid User"}
        except Exception as exp:
            data = {"detail": f"Client Error: {exp}", "code": 400}
        finally:
            return JsonResponse(data)


class ChangePassword(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        user = get_object_or_404(User, username=request.user)
        try:
            if authenticate(
                username=self.request.user.username,
                password=self.request.POST.get("password"),
            ):
                # authenticate the user
                user.set_password(self.request.POST.get("newpassword"))
                user.save()
                response = {"detail": "Password changed", "code": 200}
            else:
                response = {
                    "detail": "Cannot Authenticate User, perhaps Old Password is wrong?",
                    "code": 401,
                }
        except Exception as exp:
            response = {"detail": f"Client Error: {exp}", "code": 400}
        finally:
            return JsonResponse(response)



class ProfileCreateAPIView(generics.CreateAPIView):
    """
        Allows Creation of Profile  to User
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Profile Creation Success",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": [f"Client Error: {exp}"]})


class UsersProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            qs = UserProfile.objects.all()
            active = self.request.GET.get("active")
            lga_pk = self.request.GET.get("lga_pk")
            state_pk = self.request.GET.get("state_pk")
            user_type = self.request.GET.get("user_type")
            group_pk = self.request.GET.get("group_pk")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            if lga_pk:
                qs = qs.filter(lga=lga_pk)
            if state_pk:
                qs = qs.filter(state=state_pk)
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


class ProfileDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a UserProfile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()
    lookup_field = "pk"


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of UserProfile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [MyGenericViewset]
    queryset = UserProfile.objects.all()
    lookup_field = "pk"


class MarchantListAPIView(generics.ListAPIView):
    serializer_class = MarchantSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Marchant.objects.all()


class BranchListAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Store.objects.all()

