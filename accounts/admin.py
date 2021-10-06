from django.contrib import admin
from .models import UserProfile, Marchant, Store

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname", "gender", "state_title",
                    "lga_title", "company", "active"]
    list_filter = ["active", "gender", "company", "state"]


class BranchInline(admin.TabularInline):
    extra = 1
    model = Store

@admin.register(Marchant)
class MarchantAdmin(admin.ModelAdmin):
    inlines = [BranchInline]
    list_display = ["title", "lga", "state", "branches", "active"]
    list_filter = ["active", "state", "lga"]

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "lga", "state", "active"]
    list_filter = ["active", "company", "state", "lga"]

