from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django import urls as urlresolvers
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls.exceptions import NoReverseMatch
from django.db import models
from rest_framework import status
from accounts.models import Cast
from core.abstract_models import TimeStampedModel, VODModel
from core.utils.units import LongUniqueId, getUniqueId
from core.choices import ACCESS_LEVEL_CHOICE, COMMENT_STATUS_CHOICE, POST_STATUS_CHOICE, PROMOTION_LOCATION_CHOICE, PROMOTION_TYPE_CHOICE, REVIEW_RATING_CHOICE
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, Avg

# Create your models here.

def movie_locations(instance, filename):
    return f"movies/{instance.title}/video/{filename}"

def movie_thumb_locations(instance, filename):
    return f"movies/{instance.title}/thumb/{filename}"

def episode_location(instance, filename):
    return f"series/{instance.series.title}/{instance.title}/video/{filename}"
    
def episode_thumb_location(instance, filename):
    return f"series/{instance.series.title}/{instance.title}/thumb/{filename}"

class Category(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    uid = models.CharField(default=getUniqueId, unique=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        # if getattr(self, '_title_changed', True):
        #     small = rescale_image(self.image, width=100, height=100)
        self.title = f"{self.title}".title()
        super(Category, self).save(*args, **kwargs)

    def get_form_format(self):
        dta = {
            "pk": self.pk,
            "title": self.title,
            "status": self.status,
        }
        cat_movies = self.movies.filter(status="published").order_by("-timestamp")[:4]
        cat_series = self.series.filter(status="published").order_by("-timestamp")[:4]
        dta["movies"] = [ m.get_form_format() for m in cat_movies ]
        dta["series"] = [s.get_form_format() for s in cat_series ]
        return dta

    def __str__(self) -> str:
        return f"{self.title}"

class Genre(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    uid = models.CharField(default=getUniqueId, unique=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)

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
    casts = models.ManyToManyField(Cast, blank=True,)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="movies")
    release_year = models.PositiveIntegerField()
    running_time = models.CharField(max_length=20,blank=True, null=True)
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

    @property
    def get_data_type(self):
        return "movie"

    @property
    def get_thumb_url(self):
        if self.thumb:
            return self.thumb.url

    @property
    def category_title(self):
        if self.category:
            return f"{self.category}"

    @property
    def get_genres(self):
        dta = [g.title for g in self.genres.all()]
        return dta

    @property
    def get_casts(self):
        dta = self.casts.all().values("pk", "fullname", "nickname")
        return dta
        
    def get_posters(self):
        dta = [g.get_form_format() for g in self.posters.all()]
        return dta

    def get_rating(self):
        try:
            qs = Review.objects.all()
            target_content_type = ContentType.objects.get(app_label='vod', model="movie")
            dta = qs.filter(content_type=target_content_type, object_id=self.pk)
            dta_count = dta.count()
            # print(dta_count)
            # dta_dum  = sum(map(int, dta.values_list("rate", flat=True)))
            # dta_dum = dta.aggregate(Sum('rate'))
            dta_dum = dta.aggregate(Avg('rate'))
            # print(dta_dum)
            # rate = dta_dum.get("rate__sum", 1)/dta_count
            rate = dta_dum.get("rate__avg", 1) #/dta_count
        except Exception as exp:
            print(exp)
            rate = 0
        return rate

    def get_form_format(self):
        dta = {
            "pk": self.pk,
            "title": self.title,
            "uid": self.uid,
            "thumb": self.get_thumb_url,
            # "category_title": self.category_title,
            "get_genres": self.get_genres,
            "status": self.status,
            "access_level": self.access_level,
        }
        return dta

    def get_related(self):
        import random
        """ Return Related Movies Based on the Current Movie"""
        related_by_genre = Movie.objects.filter(status="published", genres__in=self.genres.all())
        related_by_category = Movie.objects.filter(status="published", category=self.category)
        related_by_company = Movie.objects.filter(status="published", company=self.company)
        related = related_by_genre | related_by_category # | related_by_company
        related = related.exclude(pk=self.pk).distinct()
        related = list(related)
        random.shuffle(related)
        related = related[:10]
        dta = [m.get_form_format() for m in related ]
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
    genres = models.ManyToManyField(Genre, blank=True,)
    casts = models.ManyToManyField(Cast, blank=True,)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="series")
    release_year = models.PositiveIntegerField()
    running_time = models.CharField(max_length=20, blank=True, null=True)
    # posters = models.ManyToManyField(Poster)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICE)
    created_by = models.ForeignKey("accounts.UserProfile", on_delete=models.PROTECT, related_name="created_series")

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
        ordering = ["-timestamp", "title"]

    @property
    def get_data_type(self):
        return "series"
        
    @property
    def get_thumb_url(self):
        if self.thumb:
            return self.thumb.url
        
    @property
    def category_title(self):
        if self.category:
            return f"{self.category}"

    @property
    def get_genres(self):
        dta = [g.title for g in self.genres.all()]
        return dta

    @property
    def get_casts(self):
        dta = self.casts.all().values("pk", "fullname", "nickname")
        return dta

    def number_of_episodes(self):
        return self.episodes.all().count()

    def get_episodes(self):
        dta = [
            episode.get_form_format() for episode in self.episodes.all().order_by("pk")
        ]
        return dta

    def get_rating(self):
        try:
            qs = Review.objects.all()
            target_content_type = ContentType.objects.get(app_label='vod', model="series")
            dta = qs.filter(content_type=target_content_type, object_id=self.pk)
            # dta_count = dta.count()
            dta_dum = dta.aggregate(Avg('rate'))
            rate = dta_dum.get("rate__avg", 0)
        except Exception as exp:
            # print(exp)
            rate = 0
        return rate

    def get_form_format(self):
        dta = {
            "pk": self.pk,
            "title": self.title,
            "uid": self.uid,
            "thumb": self.get_thumb_url,
            # "category_title": self.category_title,
            # "get_genres": self.get_genres,
            "status": self.status,
            "access_level": self.access_level,
        }
        return dta

    def get_related(self):
        import random
        """ Return Related Movies Based on the Current Movie"""

        related_by_genre = Series.objects.filter(status="published", genres__in=self.genres.all())
        related_by_category = Series.objects.filter(status="published", category=self.category)
        related_by_company = Series.objects.filter(status="published", company=self.company)
        related = related_by_genre | related_by_category # | related_by_company
        related = related.exclude(pk=self.pk).distinct()
        related = list(related)
        random.shuffle(related)
        related = related[:10]
        dta = [m.get_form_format() for m in related]
        return dta

    def __str__(self):
        return self.title


class SeriesEpisode(TimeStampedModel, VODModel):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=250)
    uid = models.UUIDField(default=LongUniqueId)
    thumb = models.ImageField(upload_to=episode_thumb_location)
    description = models.TextField(blank=True, null=True)
    # posters = models.ManyToManyField(Poster, blank=True)
    video = models.FileField(upload_to=episode_location)
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICE)
    # access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICE)
    uploaded_by = models.ForeignKey("accounts.UserProfile", on_delete=models.PROTECT, related_name="uploaded_episodes")


    class Meta:
        verbose_name = 'Series Episode'
        verbose_name_plural = 'Series Episodes'
        ordering = ["-timestamp", "title"]

    @property
    def get_data_type(self):
        return "series episode"

    def get_rating(self):
        try:
            qs = Review.objects.all()
            target_content_type = ContentType.objects.get(app_label='vod', model="seriesepisode")
            dta = qs.filter(content_type=target_content_type, object_id=self.pk)
            dta_count = dta.count()
            # print(dta_count)
            dta_dum = sum(map(int, dta.values_list("rate", flat=True)))
            # print(dta_dum)
            rate = dta_dum/dta_count
        except Exception as exp:
            # print(exp)
            rate = 0
        return rate

    def get_form_format(self):
        dta = {
            "pk": self.pk,
            "title": self.title,
            "thumb": self.thumb.url,
            "status": self.status,
        }
        return dta

    def series_title(self):
        return f"{self.series}"
        
    def __str__(self):
        return self.title

# Comments and Reviews
class Comment(TimeStampedModel):
    limit = models.Q(app_label='vod', model='movie') | models.Q(app_label='vod', model='series') | models.Q(app_label='vod', model='seriesepisode')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit,
                                    blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.BigIntegerField(verbose_name=_("PK of Movie, Serie or Series Episode"), blank=True, null=True,)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField(max_length=255, verbose_name=_("object representation"), blank=True, null=True)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=255)
    status = models.CharField(max_length=25, choices=COMMENT_STATUS_CHOICE)

    # Metadata
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        self.object_repr = f"{obj}"
        super(Comment, self).save(*args, **kwargs)

    def get_data_type(self):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        return obj.get_data_type

    def resource_url(self):
        app_label, model = self.content_type.app_label, self.content_type.model
        viewname = "admin:%s_%s_change" % (app_label, model)
        try:
            # args = [self.object_pk] if self.object_id is None else [self.object_id]
            args = [self.object_id]
            link = urlresolvers.reverse(viewname, args=args)
        except NoReverseMatch:
            return self.object_repr
        else:
            return format_html('<a href="{}">{}</a>', link, self.object_repr)
    
    def author_title(self):
        return f"{self.author}"

    def __str__(self):
        return f"{self.author} Comment on: {self.object_repr}"

class Review(TimeStampedModel):
    limit = models.Q(app_label='vod', model='movie') | models.Q(
        app_label='vod', model='series') | models.Q(app_label='vod', model='seriesepisode')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit,
                                     blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.BigIntegerField(verbose_name=_("PK of Movie, Serie or Series Episode"), blank=True, null=True,)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField(max_length=255, verbose_name=_("object representation"), blank=True, null=True)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(max_length=255)
    rate = models.CharField(max_length=1, choices=REVIEW_RATING_CHOICE, help_text="Rating Stars")
    status = models.CharField(max_length=25, choices=COMMENT_STATUS_CHOICE)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        self.object_repr = f"{obj}"
        super(Review, self).save(*args, **kwargs)

    def get_data_type(self):
        ct = ContentType.objects.get_for_id(self.content_type.pk)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        return obj.get_data_type

    def resource_url(self):
        app_label, model = self.content_type.app_label, self.content_type.model
        viewname = "admin:%s_%s_change" % (app_label, model)
        try:
            args = [self.object_id]
            link = urlresolvers.reverse(viewname, args=args)
        except NoReverseMatch:
            return self.object_repr
        else:
            return format_html('<a href="{}">{}</a>', link, self.object_repr)

    def author_title(self):
        return f"{self.author}"
        
    def __str__(self):
        return f"{self.author} Review on: {self.object_repr}"


## ADS | Sliders

class Promotion(TimeStampedModel):
    # uid = models.SlugField(default=LongUniqueId)
    title = models.CharField(max_length=50, blank=True, null=True)
    uid = models.CharField(default=getUniqueId, unique=True, max_length=10)
    type = models.CharField(max_length=10, choices=PROMOTION_TYPE_CHOICE)
    limit = models.Q(app_label = 'vod', model='movie') | models.Q(app_label='vod', model='series')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.BigIntegerField(verbose_name=_("PK of Movie or a Serie"), blank=True, null=True,)
    content_object = GenericForeignKey('content_type', 'object_id')
    poster = models.ImageField(upload_to="promotions",)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=50, choices=PROMOTION_LOCATION_CHOICE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        ordering = ["-updated"]


    def clean(self):
        # self.is_cleaned = True
        # TODO: rewrite logic
        if not (self.content_type and self.object_id) and not (self.poster):
            raise ValidationError("You Must Provide (content_type and PK of Movie or a Serie) or a Poster Image")
        super(Promotion, self).clean()

    def save(self, *args, **kwargs):
        # if not self.is_cleaned:
        self.full_clean()
        super(Promotion, self).save(*args, **kwargs)

    def get_obj_access_level(self):
        # check conditions
        if self.content_type and self.object_id:
            obj = self.content_type.get_object_for_this_type(pk=self.object_id)
            return f"{obj.access_level}"
    
    def __str__(self):
        return f"{self.type.title()} Promotion: {self.uid}"


