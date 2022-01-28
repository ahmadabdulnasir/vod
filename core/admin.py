from django.contrib import admin


from .models import MainPage, HomePageSlider, SliderImage, Partner, SiteInformation



class MainPageAdmin(admin.ModelAdmin):
    list_display = ("title", "timestamp", "on_navigation")
    search_fields = ["title", "sub_title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["timestamp", "updated"]


class SliderInline(admin.TabularInline):
    model = SliderImage


# class SliderButtonInline(admin.TabularInline):
#     model = SliderButton


class SliderAdmin(admin.ModelAdmin):
    inlines = [SliderInline]

    class Meta:
        model = HomePageSlider


class SiteInformationAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ["title", "info", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["timestamp", "updated"]


# Register your models here.
admin.site.register(MainPage, MainPageAdmin)
# admin.site.register(HomePageSlider, SliderAdmin)
# admin.site.register(Partner)
admin.site.register(SiteInformation, SiteInformationAdmin)