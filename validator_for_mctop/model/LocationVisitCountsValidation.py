from django.db import models


class LocationVisitCountsValidation(models.Model):
    duplicated_locations = models.CharField(max_length=100, blank=True, null=True)
    is_validated = models.BooleanField(default=False)
