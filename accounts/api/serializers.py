from core.api.serializers import CustomeSerializer
from accounts.models import UserProfile, Marchant, Store, SubscriptionPlan
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(CustomeSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "pk", 
            "user", 
            "username", 
            "profile_completed",
            "user_type", 
            "first_name",
            "last_name",
            "fullname",
            "image",
            "DOB",
            "phone_number",
            "get_email",
            "active",
            "get_films_watched",
            "get_plan",
            "subscribtion_date",
            "subscription_status",
            "comments_counts",
            "reviews_counts",
            "state",
            "address",
            # "state_title",
            # "lga",
            # "lga_title",
            "company",
            "company_title",
            "branch",
            "branch_title",
            "timestamp", 
            "updated",
            ]



class UserProfileListSerializer(CustomeSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "pk", 
            "user", 
            "username",
            "profile_completed",
            "user_type", 
            "fullname",
            "phone_number",
            "get_email",
            "active",
            # "state",
            # "state_title",
            # "lga",
            # "lga_title",
            # "company",
            # "company_title",
            # "branch",
            # "branch_title",
            "timestamp", 
            "updated",
            ]


class MarchantSerializer(CustomeSerializer):

    class Meta:
        model = Marchant
        fields = [
            "pk", 
            "title",
            "logo", 
            "hq_address", 
            "state", 
            # "state_title", 
            "lga", 
            # "lga_title",
            "get_plan",
            "subscribtion_date",
            "active", 
            "timestamp", 
            "updated",
            ]


class StoreSerializer(CustomeSerializer):

    class Meta:
        model = Store
        fields = [
            "pk",
            "title",
            "company",
            "address",
            "state",
            # "state_title",
            "lga",
            # "lga_title",
            "active",
            "timestamp",
            "updated",
        ]


class SubscriptionPlanSerializer(CustomeSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = [
            "pk",
            "name",
            "price",
            "duration",
            "plan_type",
            "active",
            "timestamp",
            "updated",
        ]
