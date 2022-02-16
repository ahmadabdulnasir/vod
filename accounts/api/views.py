from django.contrib.auth import models
from core.location.models import LGA, State
from accounts.models import  Cast, SubscriptionPlan, UserProfile, Marchant, Store, PasswordResetTokens
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
    CastDetailsSerializer,
    CastListSerializer,

)

from core.utils.varname.helpers import Wrapper
from django.utils import timezone
from django.core.validators import validate_email

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
        gender = request.POST.get("gender")
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
            # "gender" : gender,
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
            try:
                user.set_password(password)
                user.email = email
                # user.first_name = first_name
                # user.last_name = last_name
                user.save()
            except Exception as exp:
                user.delete()
                raise ValidationError({"detail": f"An Error Occured while creating User: {exp}"})
            
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
                if user_type:
                    egg["user_type"] = user_type
                if state:
                    egg["state"] = state
                if gender:
                    egg["gender"] = gender
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


class ResetPassword(APIView):
    """Allow a User to reset their Login Password
    """
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        token = request.POST.get("token")
        new_password_1 = request.POST.get("new_password_1")
        new_password_2 = request.POST.get("new_password_2")
        reset = None
        if (
            not token
            or not new_password_1
            or not new_password_2
        ):
            dta = {
                "detail": "Please Provide : token, new_password_1 and new_password_2", "code": 400
            }
            raise ValidationError(dta)
        try:
            reset = PasswordResetTokens.objects.get(token=token, active=True)
            if reset and reset.active:
                user = reset.user
                user.set_password(new_password_1)
                user.save()
                dta = {"detail": "Password changed Successfully"}
                status_code = 200
                reset.active = False
                reset.save()
            else:
                dta = {
                    "detail": "Password cannot be changed. Expired Token!!!",
                }
                status_code = 400
        except PasswordResetTokens.DoesNotExist as exp:
            raise ValidationError(
                {
                    "details": "Invalid Token!!!"
                }
            )
        except Exception as exp:
            print("here")
            dta = {"detail": f"Client Error: {exp}"}
            status_code = 400
        finally:
            return Response(data=dta, status=status_code)

    def get(self, request, format="json"):
        username = request.GET.get("username")
        email = request.GET.get("email")
        if ( not username and not email):
            dta = {
                "detail": "Please Provide one of : username or email",
            }
            raise ValidationError(dta)
        dta_success = {"detail": "An OTP Code was sent to your registered Email"}
        dta_error = {"detail": "An Error Occured"}
        user = None
        status_code = 200
        try:
            user = User.objects.get(username=username)
            reset, created = PasswordResetTokens.objects.get_or_create(user=user,active=True)
            dta = dta_success
            # if not created:
            reset.email_user()
        except User.DoesNotExist as exp:
            print("Username: ", exp)
            try:
                print("Using Email: ", email)
                try:
                    validate_email(email)
                # except ValidationError as exp:
                except Exception as exp:
                    print("Bad email: ", exp)
                    raise ValidationError(
                        {
                            "details": f"Invalid Email: {email}"
                        }
                    )
                else:
                    user = User.objects.get(email=email)
                    reset, created = PasswordResetTokens.objects.get_or_create(
                        user=user, active=True
                    )
                    dta = dta_success
                    # if not created:
                    reset.email_user()
            except User.DoesNotExist as exp:
                print("Email: ", exp)
                dta = {"detail": f"Client Error: {exp}"}
                status_code = 400
        except Exception as exp:
            dta = {"detail": f"Client Error: {exp}"}
            status_code = 400
        finally:
            if user and not user.email:
                print("No email")
                raise ValidationError(
                    {
                        "details": f"User: {user} has no email Address"
                    }
                )
            return Response(data=dta, status=status_code)


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

class UpgradeUserAccountAPIView(APIView):
    """
       Allows Upgrading an Account to a Premium User Account
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format="json"):
        today = timezone.now()
        subscription_plan_pk = request.data.get("subscription_plan_pk")
        # active = request.data.get("active")
        error_list = []
        required_info = {
            # "profile_pk": profile_pk,
            "subscription_plan": subscription_plan_pk,
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
            assert(subscription_plan.plan_type == "users")
            print(f"Plan OK. {subscription_plan}")
        except SubscriptionPlan.DoesNotExist as exp:
            plan_error_list.append(exp)
        except Exception as exp:
            plan_error_list.append(exp)
        finally:
            if plan_error_list:
                print(f"Error: {plan_error_list}")
                status_code = 406
                dta = {
                    "detail": "Fail to Upgrade Account, Invalid Subscription Plan.",
                    "errors": error_list,
                }
                raise ValidationError(dta, code=status_code)
        # profile = get_object_or_404(UserProfile, pk=profile_pk)
        profile = request.user.profile
        profile_serializer = UserProfileSerializer(profile, context={'request': request})
        if not profile.profile_completed():
            status_code = 406
            dta = {
                "detail": "Fail to Upgrade Account, Please Complete your Profile First.",
                "errors": ["Incomplete Profile"],
                "profile": profile_serializer.data
            }
            raise ValidationError(dta, code=status_code)
        # try:
        profile.user_type = "premium_user"
        # print(subscription_plan)
        profile.plan = subscription_plan
        profile.subscribtion_date = today.date()
        profile.save()
        dta = {
            "message": "Account Upgraded Successfully.",
            "profile": profile_serializer.data,
        }
        
        status_code = status.HTTP_200_OK
        # except Exception as exp:
        #   msg = f"Error while upgrading profile for the user: {exp}"
        #   raise ValidationError(
        #       {"detail": f"{msg}"}
        #   )
        return Response(dta, status=status_code)

class CreateUpdateMarchantAccountAPIView(APIView):
    """
       Allows Create/Update Marchant Account
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format="json"):
        today = timezone.now()
        title = request.POST.get("title")
        logo = request.FILES.get("logo")
        hq_address = request.POST.get("hq_address")
        lga = request.POST.get("lga")
        state = request.POST.get("state")
        profile = request.user.profile
        error_list = []
        required_info = {
            "title": title,
            "logo": logo,
            "hq_address": hq_address,
            "lga": lga,
            "state": state,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Create Merchant Account, Non or Partial Data Received.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, code=status_code)
        try:
            profile_serializer = UserProfileSerializer(profile, context={'request': request})
            if not profile.company:
                marchant_data = Marchant(
                    title=title,
                    logo=logo,
                    hq_address=hq_address,
                    lga=f"{lga}".upper(),
                    state=f"{state}".upper(),
                    # plan=subscription_plan,
                    # subscribtion_date=today.date(),
                    created_by=profile,
                )
                marchant_data.save()
                profile.company = marchant_data
            else:
                marchant_data = profile.company
                marchant_data.title = title
                marchant_data.logo=logo
                marchant_data.hq_address=hq_address
                marchant_data.lga=f"{lga}".upper()
                marchant_data.state = f"{state}".upper()
                marchant_data.save()

            # marchant_data = profile.company
            # marchant_data.plan = subscription_plan
            marchant_data.subscribtion_date = today.date()
            profile.user_type = "marchant"
            profile.save()
            dta = {
                "message": "Merchant Account Successfully Updated.",
                "profile": profile_serializer.data,
            }

            status_code = status.HTTP_200_OK
        except Exception as exp:
          msg = f"Error while upgrading profile for the user: {exp}"
          raise ValidationError(
              {"detail": f"{msg}"}
          )
        return Response(dta, status=status_code)

class UpdateAccountToMarchantAPIView(APIView):
    """
       Allows Upgrading Account to a Marchant Account
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format="json"):
        today = timezone.now()
        subscription_plan_pk = request.data.get("subscription_plan_pk")
        error_list = []
        required_info = {
            "subscription_plan": subscription_plan_pk,
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
        # Getting Profile Data
        profile = request.user.profile
        # Validate subscription_plan
        plan_error_list = []
        try:
            subscription_plan = SubscriptionPlan.objects.get(pk=subscription_plan_pk)
            assert(subscription_plan.plan_type == "marchants")
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
        # try:
        profile_serializer = UserProfileSerializer(profile, context={'request': request})
        if not profile.company:
            status_code = 406
            dta = {
                "detail": "Fail to Upgrade Account, User Has no Company Profile.",
                # "errors": error_list,
            }
            raise ValidationError(dta, code=status_code)
        marchant_data = profile.company
        marchant_data.plan = subscription_plan
        marchant_data.subscribtion_date = today.date()
        marchant_data.save()
        profile.user_type = "marchant"
        profile.save()
        dta = {
            "message": "Account Upgraded Successfully.",
            "profile": profile_serializer.data,
        }
        
        status_code = status.HTTP_200_OK
        # except Exception as exp:
        #   msg = f"Error while upgrading profile for the user: {exp}"
        #   raise ValidationError(
        #       {"detail": f"{msg}"}
        #   )
        return Response(dta, status=status_code)


class MarchantCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Marchant
    """
    serializer_class = MarchantSerializer
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

class MarchantListAPIView(generics.ListAPIView):
    """
       List All Marchant
    """
    serializer_class = MarchantSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Marchant.objects.all()
            active = self.request.GET.get("active")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

class MarchantDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of Marchant
    """
    serializer_class = MarchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Marchant.objects.all()
    lookup_field = "pk"

class MarchantUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Marchant
    """
    serializer_class = MarchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Marchant.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()
        dta = {
            "detail": "Update Success",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_200_OK)

class MarchantDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Marchant
    """
    serializer_class = MarchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Marchant.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Marchant: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

class BranchListAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Store.objects.all()


## SubscriptionPlan

class SubscriptionPlanCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a SubscriptionPlan
    """
    serializer_class = SubscriptionPlanSerializer
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

class SubscriptionPlanListAPIView(generics.ListAPIView):
    """
       List All SubscriptionPlan
    """
    serializer_class = SubscriptionPlanSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = SubscriptionPlan.objects.all()
            active = self.request.GET.get("active")
            plan_type = self.request.GET.get("plan_type")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            if plan_type and plan_type in ["users", "marchants"]:
                qs = qs.filter(plan_type=plan_type)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

class SubscriptionPlanDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of SubscriptionPlan
    """
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubscriptionPlan.objects.all()
    lookup_field = "pk"

class SubscriptionPlanUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating SubscriptionPlan
    """
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubscriptionPlan.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()
        dta = {
            "detail": "Update Success",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_200_OK)

class SubscriptionPlanDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a SubscriptionPlan
    """
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubscriptionPlan.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Plan: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


# cast
class CastCreateAPIView(generics.CreateAPIView):
    """
        Allow Authenticated User to Create a Cast
    """
    serializer_class = CastDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Cast Created Success",
                "data": serializer.data,
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save()


class CastListAPIView(generics.ListAPIView):
    """
       List All Cast
    """
    serializer_class = CastListSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Cast.objects.all()
            active = self.request.GET.get("active")
            if active and active == 'yes':
                qs = qs.filter(active=True)
            if active and active == 'no':
                qs = qs.filter(active=False)
            
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

class CastSearchAPIView(generics.ListAPIView):
    """
       List All Cast based on search
    """
    serializer_class = CastListSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Cast.objects.all()
            search_query = self.request.GET.get("search_query")
            if search_query:
                fullname_qs = qs.filter(fullname__icontains=search_query)
                nickname_qs = qs.filter(nickname__icontains=search_query)
                qs = fullname_qs | nickname_qs
            else:
                qs = None
            
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class CastDetailsAPIView(generics.RetrieveAPIView):
    """
       Return Details of Cast
    """
    serializer_class = CastDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Cast.objects.all()
    lookup_field = "pk"


class CastUpdateAPIView(generics.UpdateAPIView):
    """
       Allow Updating Cast
    """
    serializer_class = CastDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cast.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()
        dta = {
            "detail": "Update Success",
            "data": serializer.data,
        }
        return Response(dta, status=status.HTTP_200_OK)


class CastDeleteAPIView(generics.DestroyAPIView):
    """
        Allow Authenticated User to Delete a Cast
    """
    serializer_class = CastDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cast.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Cast: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

# ./cast
