from django.db import models
from django.db.models.query_utils import Q
from core.abstract_models import TimeStampedModel
from django.conf import settings
from core.location.nigeria_states import NIGERIA_STATES
from core.choices import (
    DURATION_CHOICE,
    GENDER_CHOICE,
    PLAN_TYPE_CHOICE,
    USER_TYPE_CHOICE
)
from django.utils import timezone, timesince
from django.urls import reverse
from django.core.validators import MinValueValidator
from core.location.models import State, LGA
from core.utils.helpers import get_duration_as_days

from core.utils.units import LongUniqueId, genserial
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

# Create your models here.


def user_image_location(instance, filename):
    return f"users/{instance.user}/images/{filename}"


def marchant_image_location(instance, filename):
    return f"marchants/{instance.title}/logo/{filename}"

def cast_image_location(instance, filename):
    return f"cast/{instance.fullname}/images/{filename}"

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
    # email = models.EmailField(max_length=50)
    DOB = models.DateField(help_text="Date of Birth", blank=True, null=True,)
    address = models.CharField(max_length=100, blank=True, null=True)
    # lga = models.ForeignKey(LGA, blank=True, null=True, on_delete=models.SET_NULL, related_name="users")
    # state = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name="users")
    state = models.CharField(max_length=50, blank=True, null=True, choices=NIGERIA_STATES)
    company = models.ForeignKey("accounts.Marchant", blank=True, null=True, on_delete=models.CASCADE, related_name="company_staffs")
    branch = models.ForeignKey("accounts.Store", blank=True, null=True,
                            on_delete=models.CASCADE, related_name="branch_staffs")
    plan = models.ForeignKey("SubscriptionPlan", limit_choices_to=Q(
        plan_type="users"), related_name="users", on_delete=models.SET_NULL, blank=True, null=True)
    subscribtion_date = models.DateField(blank=True, null=True)
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
        k1 = self.first_name if self.first_name else ""
        k2 = self.last_name if self.last_name else ""
        k = f"{k1} {k2}"
        if k == " ":
            return None
        return k

    def get_email(self):
        return f"{self.user.email}"

    def get_films_watched(self):
        return 13

    def get_plan(self):
        if self.plan:
            dta = self.plan.get_form_format()
        else:
            dta = {
                "pk": -9,
                "name": "Free Plan",
                "price": 0.0,
                "duration": None,
                "plan_type": None,
                "active": True,
            }
        return dta
        
    def comments_counts(self):
        return self.comments.all().count()

    def reviews_counts(self):
        return self.reviews.all().count()

    def profile_completed(self):
        gender_check = True if self.gender != "others" else False
        check = bool(
            self.image and self.first_name and self.last_name and 
            self.DOB and self.address and self.state and gender_check
            )
        # if self.user_type == "marchant":
        #     if self.company:
        #         marchant_check = self.company.data_completed()
        #     else:
        #         marchant_check = False
        #     check = bool(check and marchant_check)
        return check

    def subscription_status(self):
        today = timezone.now()
        plan_check = True if self.plan else False
        subscribtion_date_check = True if self.subscribtion_date else False
        egg = get_duration_as_days()
        
        if plan_check and subscribtion_date_check:
            days_difference = today.date() - self.subscribtion_date
            duration = egg.get(self.plan.duration)
            expiry_check = True if (days_difference.days < duration) else False
        else:
            expiry_check = False
        check = bool(
            plan_check and subscribtion_date_check and expiry_check
            )
        if check:
            dta = "Active"
        else:
            dta = "Expired"
        return dta

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        url = reverse("accounts:admin-edit-user", kwargs=kwargs)
        return url

    def __str__(self):
        if self.fullname():
            return f"{self.fullname()}"
        else:
            return f"{self.user}"


class Marchant(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to=marchant_image_location)
    hq_address = models.CharField(max_length=250)
    # lga = models.ForeignKey(LGA, on_delete=models.PROTECT, related_name="marchants")
    # state = models.ForeignKey(State, on_delete=models.PROTECT, related_name="marchants")
    lga = models.CharField(max_length=50,)
    state = models.CharField(max_length=50, choices=NIGERIA_STATES)
    plan = models.OneToOneField("SubscriptionPlan", limit_choices_to=Q(
        plan_type="marchants"), related_name="marchants", on_delete=models.SET_NULL, blank=True, null=True)
    subscribtion_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Marchant"
        verbose_name_plural = "Marchants"
        ordering = ["-updated",]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".title()
        super(Marchant, self).save(*args, **kwargs)

    def branches(self):
        return self.stores.all().count()

    def get_plan(self):
        if self.plan:
            dta = self.plan.get_form_format()
        else:
            dta = {
                "pk": -9,
                "name": "Free Plan (Marchant)",
                "price": 0.0,
                "duration": None,
                "plan_type": None,
                "active": True,
            }
        return dta

    def data_completed(self):
        check = bool(
            self.title and self.logo and self.logo and self.hq_address
            and self.lga and self.state and self.active

        )
        return check

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


class SubscriptionPlan(TimeStampedModel):
    """This model define types of subcriptions available on the platform
    """
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(1000.0)])
    duration = models.CharField(max_length=20, choices=DURATION_CHOICE)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICE, default="users")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscriptions Plans"
        ordering = ["-timestamp"]


    def get_form_format(self):
        dta = {
            "pk": self.pk,
            "name": self.name,
            "price": self.price,
            "duration": self.get_duration_display(),
            "plan_type": self.get_plan_type_display(),
            "active": self.active,
        }
        return dta

    def __str__(self):
        return f"{self.name} (₦{self.price}/{self.duration})"
        


class PasswordResetTokens(TimeStampedModel):
    """ 
        Model for the storing Password Reset Tokens
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="password_reset_tokens", on_delete=models.CASCADE
    )
    token = models.CharField(max_length=10, default=genserial, unique=True)
    active = models.BooleanField(default=True)
    sent_count = models.PositiveIntegerField(default=0)
    expired_time = models.DateTimeField()
    #history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Passwords Reset Tokens"
        ordering = ("-updated", )
        # unique_together = ("user", "active",)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.expired_time:
            # self.expired_time = now + timedelta(hours=1)
            self.expired_time = now + timedelta(minutes=30)
        super(PasswordResetTokens, self).save(*args, **kwargs)

    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    def get_email(self):
        return self.user.email

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def get_expired(self):
        now = timezone.now()
        if now > self.expired_time:
            expired_time = "Expired"
        else:
            expired_time = self.expired_time
        # obj.starts += timedelta(days=1, hours=2)
        return expired_time

    def email_user(self):
        # if not self.user.email:
        #     print("no email")
        #     raise Exception(f"User: {self.user} has no email Address")
        subject = "PASSWORD RESET | AREWA CINEMA"
        signature = "ArewaCinema"
        html_message = render_to_string(
            template_name="core/accounts/password_reset_mail_template.html", 
            context={
                "subject": subject,
                "details": self,
                "signature": signature,
            }
        )
        msg = strip_tags(html_message)

        try:
            # print("email: ", self.user.email)
            status = send_mail(
                subject=subject,
                message=msg,
                html_message=html_message,
                from_email=settings.SERVER_EMAIL,
                recipient_list=[self.user.email,],
                fail_silently=False,
            )
            self.sent_count += 1
            self.save()
        except Exception as exp:
            print(exp)
            status = 0
            # raise ValidationError(f"User: {self.user} has no email Address")
        finally:
            return status


    def __str__(self):
        return f"{self.fullname}"


class Cast(TimeStampedModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name="cast_profile")
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICE,)
    image = models.ImageField(upload_to=cast_image_location, blank=True, null=True,)
    bio = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cast Profile"
        verbose_name_plural = "Casts Profiles"
        ordering = ["-updated", "fullname",]

    def __str__(self) -> str:
        return f"{self.fullname}"
