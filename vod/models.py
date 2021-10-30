from django.contrib.contenttypes.models import ContentType
from django import urls as urlresolvers
from django.utils.html import format_html
from django.urls.exceptions import NoReverseMatch
from django.db import models
from django.db.models.fields import CharField
from core.abstract_models import TimeStampedModel, VODModel
from core.utils.units import LongUniqueId, getUniqueId
from core.choices import ACCESS_LEVEL_CHOICE, COMMENT_STATUS_CHOICE, POST_STATUS_CHOICE
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

# Create your models here.

def movie_locations(instance, filename):
    return f"movies/{instance.title}/video/{filename}"

def movie_thumb_locations(instance, filename):
    return f"movies/{instance.title}/thumb/{filename}"

def episode_location(instance, filename):
    return f"series/{instance.season.series.title}/{instance.season.title}/{instance.title}/video/{filename}"
    
def episode_thumb_location(instance, filename):
    return f"series/{instance.season.series.title}/{instance.season.title}/{instance.title}/thumb/{filename}"


class Category(TimeStampedModel):
    title = models.CharField(max_length=50,)
    uid = models.CharField(default=getUniqueId, unique=True, max_length=10)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        # if getattr(self, '_title_changed', True):
        #     small = rescale_image(self.image, width=100, height=100)
        self.title = f"{self.title}".title()
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"

class Genre(TimeStampedModel):
    title = models.CharField(max_length=50,)
    uid = models.CharField(default=getUniqueId, unique=True, max_length=10)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        # if getattr(self, '_image_changed', True):
        #     small = rescale_image(self.image, width=100, height=100)
        self.title = f"{self.title}".title()
        super(Genre, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"


class Movie(TimeStampedModel, VODModel):
    title = models.CharField(max_length=250)
    uid = models.UUIDField(default=LongUniqueId)
    thumb = models.ImageField(upload_to=movie_thumb_locations)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, blank=True,)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="movies")
    # posters = models.ManyToManyField(Poster, blank=True,)
    video = models.FileField(upload_to=movie_locations, blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICE)
    uploaded_by = models.ForeignKey("accounts.UserProfile", on_delete=models.PROTECT, related_name="uploaded_movies")


    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ["-timestamp", "title"]

    def category_title(self):
        if self.category:
            return f"{self.category}"

    def get_genres(self):
        dta = [g.title for g in self.genres.all()]
        return dta
        
    def get_posters(self):
        dta = [g.get_form_format() for g in self.posters.all()]
        return dta

    def __str__(self):
        return self.title


class MoviePoster(TimeStampedModel, VODModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="posters")
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="posters")
    uid = models.UUIDField(default=LongUniqueId)

    class Meta:
        verbose_name = 'Movie Poster'
        verbose_name_plural = 'Movies Posters'
        ordering = ["-updated"]

    @property
    def name(self):
        if self.title:
            return self.title
        return self.uid

    def get_form_format(self):
        dta = {
            "name": f"{self}",
            "uid": f"{self.uid}",
            "movie": f"{self.movie}",
            "image": f"{self.image.url}",
        }
        return dta

    def __str__(self):
        return f"{self.name}"

class Series(TimeStampedModel, VODModel):
    title = models.CharField(max_length=250)
    uid = models.UUIDField(default=LongUniqueId)
    thumb = models.ImageField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="series")
    # posters = models.ManyToManyField(Poster)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
        ordering = ["-timestamp", "title"]

    def __str__(self):
        return self.title


class SeriesSeason(TimeStampedModel, VODModel):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")
    title = models.CharField(max_length=250)
    uid = models.UUIDField(default=LongUniqueId)
    thumb = models.ImageField()
    description = models.TextField(blank=True, null=True)
    # posters = models.ManyToManyField(Poster, blank=True)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)

    class Meta:
        verbose_name = 'Series Season'
        verbose_name_plural = 'Series Seasons'
        ordering = ["-timestamp", "title"]

    def __str__(self):
        return self.title


class SeasonEpisode(TimeStampedModel, VODModel):
    season = models.ForeignKey(SeriesSeason, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=250)
    uid = models.UUIDField(default=LongUniqueId)
    thumb = models.ImageField(upload_to=episode_thumb_location)
    description = models.TextField(blank=True, null=True)
    # posters = models.ManyToManyField(Poster, blank=True)
    video = models.FileField(upload_to=episode_location)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)

    class Meta:
        verbose_name = 'Season Episode'
        verbose_name_plural = 'Season Episodes'
        ordering = ["-timestamp", "title"]

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("content type"),
    )
    object_pk = models.BigIntegerField(
        db_index=True, verbose_name=_("object pk")
    )
    object_id = models.BigIntegerField(
        blank=True, db_index=True, null=True, verbose_name=_("object id")
    )
    object_repr = models.CharField(max_length=255, verbose_name=_("object representation"), blank=True, null=True)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=255)
    status = models.CharField(max_length=25, choices=COMMENT_STATUS_CHOICE)

    # Metadata
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ["-updated"]

    def resource_url(self):
        app_label, model = self.content_type.app_label, self.content_type.model
        viewname = "admin:%s_%s_change" % (app_label, model)
        try:
            args = [self.object_pk] if self.object_id is None else [self.object_id]
            link = urlresolvers.reverse(viewname, args=args)
        except NoReverseMatch:
            return self.object_repr
        else:
            return format_html('<a href="{}">{}</a>', link, self.object_repr)

    def save(self, *args, **kwargs):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        self.object_repr = f"{obj}"
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.author} Comment on: {self.object_repr}"



class Review(TimeStampedModel):
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("content type"),
    )
    object_pk = models.BigIntegerField(
        db_index=True, verbose_name=_("object pk")
    )
    object_id = models.BigIntegerField(
        blank=True, db_index=True, null=True, verbose_name=_("object id")
    )
    object_repr = models.CharField(max_length=255, verbose_name=_("object representation"), blank=True, null=True)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(max_length=255)
    status = models.CharField(max_length=25, choices=COMMENT_STATUS_CHOICE)

    # Metadata
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ["-updated"]

    def resource_url(self):
        app_label, model = self.content_type.app_label, self.content_type.model
        viewname = "admin:%s_%s_change" % (app_label, model)
        try:
            args = [self.object_pk] if self.object_id is None else [self.object_id]
            link = urlresolvers.reverse(viewname, args=args)
        except NoReverseMatch:
            return self.object_repr
        else:
            return format_html('<a href="{}">{}</a>', link, self.object_repr)

    def save(self, *args, **kwargs):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        self.object_repr = f"{obj}"
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.author} Review on: {self.object_repr}"
