from django.contrib import admin

from .models import Category, Genre, Poster, Movie, Series, SeriesSeason, SeasonEpisode


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'updated', 'title', 'uid')
    list_filter = ('timestamp', 'updated')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'updated', 'title', 'uid')
    list_filter = ('timestamp', 'updated')


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'updated',
        'company',
        'branch',
        'title',
        'image',
        'uid',
    )
    list_filter = ('timestamp', 'updated', 'company', 'branch')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'updated',
        'company',
        'branch',
        'title',
        'uid',
        'thumb',
        'description',
        'category',
        'video',
        'status',
    )
    list_filter = ('timestamp', 'updated', 'company', 'branch', 'category')
    raw_id_fields = ('genre', 'posters')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'updated',
        'company',
        'branch',
        'title',
        'uid',
        'thumb',
        'description',
        'category',
        'status',
    )
    list_filter = ('timestamp', 'updated', 'company', 'branch', 'category')
    raw_id_fields = ('genre', 'posters')


@admin.register(SeriesSeason)
class SeriesSeasonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'updated',
        'company',
        'branch',
        'series',
        'title',
        'uid',
        'thumb',
        'description',
        'status',
    )
    list_filter = ('timestamp', 'updated', 'company', 'branch', 'series')
    raw_id_fields = ('posters',)


@admin.register(SeasonEpisode)
class SeasonEpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'timestamp',
        'updated',
        'company',
        'branch',
        'season',
        'title',
        'uid',
        'thumb',
        'description',
        'video',
        'status',
    )
    list_filter = ('timestamp', 'updated', 'company', 'branch', 'season')
    raw_id_fields = ('posters',)
