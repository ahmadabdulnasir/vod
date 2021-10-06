from django.contrib import admin
from .models import State, LGA


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ["title", "LGA_ID", "state", "timestamp", "updated"]
    search_fields = ["title", "LGA_ID", "state__title"]
    list_filter = ["timestamp", "updated", "state"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["title", "State_ID", "state_code", "timestamp", "updated"]
    search_fields = ["title", "State_ID", "state_code", "zone_code"]
    list_filter = ["timestamp", "updated", "zone", "zone_code"]
