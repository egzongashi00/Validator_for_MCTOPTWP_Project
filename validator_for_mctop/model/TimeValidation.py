from django.db import models


class TimeValidation(models.Model):
    location_one_id = models.IntegerField()
    location_two_id = models.IntegerField()
    distance_between_locations = models.FloatField()
    opening_time_of_location_one = models.IntegerField()
    closing_time_of_location_one = models.IntegerField()
    opening_time_of_location_two = models.IntegerField()
    closing_time_of_location_two = models.IntegerField()
    waiting_before_opening = models.IntegerField()
    location_closed = models.BooleanField()
    time_spend_before_trip = models.FloatField()
    time_spend_at_location = models.FloatField()
    time_spend_after_trip = models.FloatField()
    max_time = models.IntegerField()
    is_validated = models.BooleanField(default=False)

