from django.contrib.auth import models
from core.location.models import LGA, State
from accounts.models import  SubscriptionPlan, UserProfile, Marchant, Store
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
    SubscriptionPlanSerializer,
    UserProfileListSerializer,
    UserProfileSerializer, 
)

from core.utils.varname.helpers import Wrapper

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
        state = request.POST.get("state")
        address = request.POST.get("address")
        user_type = request.POST.get("user_type")
        image = request.FILES.get("image")
        error_list = []
        required_info = {
            "username" : username,
            "password" : password,
            # "first_name" : first_name,
            # "last_name" : last_name,
            # "image" : image,
            "email" : email,
            "phone_number" : phone_number,
            # "DOB" : dob,
            # "state" : state,
            # "lga_pk" : lga_pk,
            # "address" : address,
            # "user_type" : user_type,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if  error_list:
            dta = {
                "detail": "Fail to Create user, Non or Partial Data Received.",
                "errors": error_list,
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
            user_with_email = User.objects.filter(email=email).exists() or UserProfile.objects.filter(email=email).exists()
            if user_with_email:
                user.delete()
                raise ValidationError({"detail": f"User with email: {email} Already Exist!"})
            
            # check for state and lga validity
            # lga = None
            # state = None
            # try:
            #     lga = get_object_or_404(LGA, pk=lga_pk)
            #     state = get_object_or_404(State,pk=state_pk)
            # except Exception as exp:
            #     raise ValidationError({"detail": "Invalid Entry for State and/or LGA."})
            
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            try:
                egg = {
                    "user": user,
                    # "user_type": user_type,
                    "image": image if image else None,
                    "first_name": first_name if first_name else None,
                    "last_name": last_name if last_name else None,
                    "phone_number": phone_number,
                    "email": email,
                    "DOB": dob if dob else None,
                    # "state": state,
                    "address": address if address else None,
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
                status_code = status.HTTP_201_CREATED
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
        username = request.POST.get("username")
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        if (
            not username
            or not oldpassword
            or not newpassword
            ):
            response = {"detail": "Please Provide : username, oldpassword and newpassword", "code": 400}
        try:
            # authenticate the user
            user = authenticate(username=username, password=oldpassword)
            if user:
                # user = get_object_or_404(User, username=username)
                user.set_password(newpassword)
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
    # queryset = UserProfile.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            qs = UserProfile.objects.all()
            active = self.request.GET.get("active")
            # lga_pk = self.request.GET.get("lga_pk")
            state = self.request.GET.get("state")
            user_type = self.request.GET.get("user_type")
            group_pk = self.request.GET.get("group_pk")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            # if lga_pk:
            #     qs = qs.filter(lga=lga_pk)
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


class UpdateAccountToMarchantAPIView(APIView):
    """
       Allows Upgrading Account to a Marchant Account
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format="json"):
        # profile_pk = request.data.get("profile_pk")
        title = request.data.get("title")
        logo = request.data.get("logo")
        hq_address = request.data.get("hq_address")
        lga = request.data.get("lga")
        state = request.data.get("state")
        subscription_plan_pk = request.data.get("subscription_plan_pk")
        # active = request.data.get("active")
        error_list = []
        required_info = {
            # "profile_pk": profile_pk,
            "title": title,
            "logo": logo,
            "hq_address": hq_address,
            "lga": lga,
            "state": state,
            "subscription_plan": subscription_plan,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Upgrade Account, Non or Partial Data Received.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)
        # Validate subscription_plan
        plan_error_list = []
        try:
            subscription_plan = SubscriptionPlan.objects.get(pk=subscription_plan_pk)
        except SubscriptionPlan.DoesNotExist as exp:
            plan_error_list.append(exp)
        except Exception as exp:
            plan_error_list.append(exp)
        finally:
            if plan_error_list:
                status_code = 406
                dta = {
                    "detail": "Fail to Upgrade Account, Invalid Subscription Plan.",
                    "errors": error_list,
                }
                raise ValidationError(dta, code=status_code)
        # profile = get_object_or_404(UserProfile, pk=profile_pk)
        profile = request.user.profile
        try:
            profile_serializer = UserProfileSerializer(profile, context={'request': request})
            marchant_data = Marchant(
                title=title,
                logo = logo,
                hq_address = hq_address,
                lga = f"{lga}".upper(),
                state = f"{state}".upper()
            )
            marchant_data.save()
            profile.user_type = "marchant"
            profile.company = marchant_data
            profile.save()
            dta = {
                "message": "Account Upgraded Successfully.",
                "profile": profile_serializer.data,
            }
            
            status_code = status.HTTP_200_OK
        except Exception as exp:
          msg = f"Error while upgrading profile for the user: {exp}"
          raise ValidationError(
              {"detail": f"{msg}"}
          )
        return Response(dta, status=status_code)


class MarchantListAPIView(generics.ListAPIView):
    serializer_class = MarchantSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Marchant.objects.all()


class BranchListAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Store.objects.all()


class SubscriptionPlanListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # queryset = SubscriptionPlan.objects.all()

    def get_queryset(self, *args, **kwargs):
        try:
            qs = SubscriptionPlan.objects.all()
            active = self.request.GET.get("active")
            plan_type = self.request.GET.get("plan_type")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            if plan_type and plan_type in []:
                qs = qs.filter(plan_type=plan_type)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

