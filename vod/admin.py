from django.contrib import admin

from .models import (
    Category,
    Genre,
    Movie,
    MoviePoster,
    Series,
    SeriesSeason,
    SeasonEpisode,
    Comment,
    Review,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'uid', 'timestamp', 'updated', )
    list_filter = ('timestamp', 'updated')
    search_fields = ("title",)
    date_hierarchy = "timestamp"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'uid', 'timestamp', 'updated',)
    list_filter = ('timestamp', 'updated')
    search_fields = ("title",)
    date_hierarchy = "timestamp"



class MoviePosterInline(admin.StackedInline):
    model = MoviePoster
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (MoviePosterInline,)
    list_display = (
        'title',
        # 'uid',
        # 'thumb',
        # 'description',
        'category',
        # 'video',
        'status',
        'company',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'category')
    search_fields = ("title", "description")
    date_hierarchy = "timestamp"


@admin.register(MoviePoster)
class MoviePosterAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'movie',
        'company',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        # 'uid',
        # 'thumb',
        # 'description',
        'category',
        'status',
        'company',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'category')
    search_fields = ("title",)
    date_hierarchy = "timestamp"


@admin.register(SeriesSeason)
class SeriesSeasonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        # 'uid',
        # 'thumb',
        # 'description',
        'status',
        'company',
        'series',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'series')
    search_fields = ("title",)
    date_hierarchy = "timestamp"


@admin.register(SeasonEpisode)
class SeasonEpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uid',
        # 'thumb',
        # 'description',
        # 'video',
        'status',
        'company',
        'season',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'season')
    search_fields = ("title",)
    date_hierarchy = "timestamp"



#
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = [
        "author", "body",
        "content_type", "object_pk", 
        "object_id", "object_repr",
    ]
    list_display = ["author", "resource_url", "status", "timestamp", "updated"]
    list_editable = ["status"]
    list_filter = ["status", "timestamp", "updated"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = [
        "author", "body",
        "content_type", "object_pk", 
        "object_id", "object_repr",
    ]
    list_display = ["author", "resource_url", "status", "timestamp", "updated"]
    list_editable = ["status"]
    list_filter = ["status", "timestamp", "updated"]





