from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import deactivate
from core.abstract_models import TimeStampedModel
from django.conf import settings
from core.location.nigeria_states import NIGERIA_STATES
from core.choices import (
    GENDER_CHOICE,
    USER_TYPE_CHOICE
)
from django.utils import timezone, timesince
from django.urls import reverse
from django.core.validators import MinValueValidator
from core.location.models import State, LGA
# Create your models here.


def user_image_location(instance, filename):
    return f"users/{instance.user}/images/{filename}"


def marchant_image_location(instance, filename):
    return f"marchants/{instance.title}/logo/{filename}"

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    user_type = models.CharField(
        max_length=50, choices=USER_TYPE_CHOICE, default="free_user"
    )
    image = models.ImageField(upload_to=user_image_location, blank=True, null=True,)
    first_name = models.CharField(max_length=50, blank=True, null=True,)
    last_name = models.CharField(max_length=50, blank=True, null=True,)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICE, default="others")
    phone_number = models.CharField(max_length=15, blank=True, null=True,)
    email = models.EmailField(max_length=50)
    DOB = models.DateField(help_text="Date of Birth", blank=True, null=True,)
    address = models.CharField(max_length=100, blank=True, null=True)
    # lga = models.ForeignKey(LGA, blank=True, null=True, on_delete=models.SET_NULL, related_name="users")
    # state = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name="users")
    state = models.CharField(max_length=50, blank=True, null=True, choices=NIGERIA_STATES)
    company = models.ForeignKey("accounts.Marchant", blank=True, null=True, on_delete=models.CASCADE, related_name="company_staffs")
    branch = models.ForeignKey("accounts.Store", blank=True, null=True,
                            on_delete=models.CASCADE, related_name="branch_staffs")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-updated", "first_name", "last_name"]

    def user_groups(self):
        return [g.name for g in self.user.groups.all()]

    def state_title(self):
        if self.state:
            return f"{self.state.title}"

    def lga_title(self):
        if self.lga:
            return f"{self.lga.title}"

    def company_title(self):
        if self.company:
            return f"{self.company.title}"

    def branch_title(self):
        if self.branch:
            return f"{self.branch.title}"

    def age(self):
        return f"{timezone.now().year-self.DOB.year}"

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_email(self):
        return f"{self.email}"

    def get_films_watched(self):
        return 13

    def get_plan(self):
        return "Free (N0/Month)"
        
    def comments_counts(self):
        return 112

    def reviews_counts(self):
        return 112

    def reviews_counts(self):
        return 112

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        url = reverse("accounts:admin-edit-user", kwargs=kwargs)
        return url

    def __str__(self):
        return f"{self.fullname()}"


class Marchant(TimeStampedModel):
    title = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=marchant_image_location)
    hq_address = models.CharField(max_length=250)
    # lga = models.ForeignKey(LGA, on_delete=models.PROTECT, related_name="marchants")
    # state = models.ForeignKey(State, on_delete=models.PROTECT, related_name="marchants")
    lga = models.CharField(max_length=50,)
    state = models.CharField(max_length=50, choices=NIGERIA_STATES)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Marchant"
        verbose_name_plural = "Marchants"
        ordering = ["-updated",]

    def state_title(self):
        if self.state:
            return f"{self.state.title}"

    def lga_title(self):
        if self.lga:
            return f"{self.lga.title}"

    def branches(self):
        return self.stores.all().count()

    def __str__(self):
        return f"{self.title}"


class Store(TimeStampedModel):
    title = models.CharField(max_length=50)
    company = models.ForeignKey("accounts.Marchant", on_delete=models.CASCADE, related_name="stores")
    address = models.CharField(max_length=250)
    lga = models.CharField(max_length=50,)
    state = models.CharField(max_length=50, choices=NIGERIA_STATES)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ["-updated", "company"]

    def state_title(self):
        if self.state:
            return f"{self.state.title}"

    def lga_title(self):
        if self.lga:
            return f"{self.lga.title}"

    def __str__(self):
        return f"{self.title} -- {self.company}"


class UserWallet(TimeStampedModel):
    profile = models.OneToOneField(
        UserProfile, related_name="wallet", on_delete=models.CASCADE
    )
    balance = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Wallet"
        verbose_name_plural = "Users Walltes"
        ordering = ["-timestamp"]

    def fullname(self):
        return f"{self.profile.fullname()}"

    def get_absolute_url(self):
        return reverse("finance:admin-wallet-crud", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.profile} --> ₦ {self.balance}"
