from django.db import models


class SequenceOfDesire(models.Model):
    sequence_of_trip = models.CharField(max_length=400)
    is_validated = models.BooleanField(default=False)

