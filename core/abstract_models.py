from django.db import models
# from accounts.models import Marchant, Store

class TimeStampedModel(models.Model):
    """
    Abstract base model with fields for tracking object creation and last
    update dates.
    """

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class POSModel(models.Model):
    """
    Abstract base model with fields for tracking object Marchant and Branch/Store
    """

    company = models.ForeignKey("accounts.Marchant", on_delete=models.CASCADE,)
    branch = models.ForeignKey("accounts.Store", on_delete=models.CASCADE,)

    class Meta:
        abstract = True
