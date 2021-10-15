from django.contrib import admin
from .models import UserProfile, Marchant, Store

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname", "gender", "state",
                    "company", "profile_completed", "active"]
    list_filter = ["active", "gender", "company", "state"]


class BranchInline(admin.TabularInline):
    extra = 1
    model = Store

@admin.register(Marchant)
class MarchantAdmin(admin.ModelAdmin):
    inlines = [BranchInline]
    list_display = ["title", "state", "branches", "active"]
    list_filter = ["active", "state",]

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "state", "active"]
    list_filter = ["active", "company", "state",]

