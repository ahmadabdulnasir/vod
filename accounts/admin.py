from django.contrib import admin
from .models import UserProfile, Marchant, Store, SubscriptionPlan, PasswordResetTokens, Cast

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname", "gender", "state", "user_type",
                    "company", "profile_completed", "plan", "subscribtion_date", "active"]
    list_filter = ["active", "gender",  "user_type", "company", "state"]
    search_fields = ["user__username", "first_name", "last_name", "user__email"]
    autocomplete_fields = ["user"]


class BranchInline(admin.TabularInline):
    extra = 1
    model = Store

@admin.register(Marchant)
class MarchantAdmin(admin.ModelAdmin):
    inlines = [BranchInline]
    list_display = ["title", "state", "branches", "plan", "subscribtion_date", "active"]
    list_filter = ["active", "state",]

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "state", "active"]
    list_filter = ["active", "company", "state",]

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "duration", "plan_type", "active", "updated"]
    list_filter = ["active", "plan_type", "duration", "timestamp", "updated"]


@admin.register(PasswordResetTokens)
class PasswordResetTokensAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "fullname",
        "get_email",
        "sent_count",
        "active",
        # "get_expired",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated", )
    autocomplete_fields = ["user"]


@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = (
        # "user",
        "fullname",
        "nickname",
        "gender",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("gender", "active", "timestamp", "updated", )
    autocomplete_fields = ["user"]
