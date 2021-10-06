from django.db import models
from core.abstract_models import TimeStampedModel

# from audit.registry import audit


class LGA(TimeStampedModel):
    title = models.CharField(max_length=50)
    LGA_ID = models.CharField(max_length=10, blank=True, null=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "LGA"
        verbose_name_plural = "LGAs"
        ordering = ["title", "state"]

    def __str__(self):
        return self.title


class State(TimeStampedModel):
    title = models.CharField(max_length=50)
    State_ID = models.CharField(max_length=10)
    state_code = models.CharField(max_length=10)
    zone = models.CharField(max_length=50)
    zone_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["title", ]

    def __str__(self):
        return self.title


# Register Models for Logging
# audit.register(LGA)
# audit.register(State)
