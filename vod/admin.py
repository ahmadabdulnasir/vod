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
        'title',
        'uid',
        'thumb',
        'description',
        'category',
        'video',
        'status',
        'company',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'category')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uid',
        'thumb',
        'description',
        'category',
        'status',
        'company',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'category')


@admin.register(SeriesSeason)
class SeriesSeasonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uid',
        'thumb',
        'description',
        'status',
        'company',
        'series',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'series')


@admin.register(SeasonEpisode)
class SeasonEpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uid',
        'thumb',
        'description',
        'video',
        'status',
        'company',
        'season',
        'timestamp',
        'updated',
    )
    list_filter = ('timestamp', 'updated', 'company', 'season')
