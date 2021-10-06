from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from core.utils import getUniqueId, LongUniqueId
from core.abstract_models import TimeStampedModel


class MainPage(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    # img = models.ForeignKey(
    #     "gallery.Image", blank=True, null=True, on_delete=models.SET_NULL
    # )
    body = RichTextUploadingField(blank=True, null=True)
    # vid_file = models.ForeignKey(
    #     "gallery.Video", blank=True, null=True, on_delete=models.SET_NULL
    # )
    youtube_video_id = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        help_text="Youtube Video ID e.g L0I7i_lE5zA. Not Complete Url",
    )
    extra_info = RichTextField(blank=True, null=True)
    on_navigation = models.BooleanField(default=False)
    # Metadata
    class Meta:
        verbose_name = "Main Page"
        verbose_name_plural = "Main Pages"
        ordering = ["-title"]

    # Methods
    def get_video_link(self):
        if self.youtube_video_id:
            return "https://www.youtube.com/embed/{}".format(self.youtube_video_id)
        elif self.vid_file:
            return self.vid_file.url
        else:
            return None

    def get_absolute_url(self):
        kwargs = {"slug": self.slug}
        url = reverse("core:page", kwargs=kwargs)
        return url

    def __str__(self):
        return self.title


class HomePageSlider(TimeStampedModel):
    title = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Home Page Slider"
        verbose_name_plural = "Home Page Sliders"
        ordering = ["-updated"]

    def __str__(self):
        return self.title


class SliderImage(TimeStampedModel):
    slider = models.ForeignKey(
        HomePageSlider, on_delete=models.CASCADE, related_name="sliders"
    )
    file = models.ImageField(
        upload_to="sliders/img",
        help_text="Image size is 1900px width and 1267px height",
    )
    header = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=300, blank=True, null=True)
    button_name = models.CharField(max_length=50, blank=True, null=True)
    button_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
        ordering = ["-updated"]

    def __str__(self):
        return self.slider.title


class Partner(TimeStampedModel):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="partners", help_text="Image size is 340x145 px")
    website = models.CharField(
        max_length=200, help_text="Start with http:// or https://"
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SiteInformation(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    info = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Information"
        verbose_name_plural = "Site Informations"
        ordering = ["-updated"]

    def get_absolute_url(self):
        return reverse("core:core-settings-edit-add", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
