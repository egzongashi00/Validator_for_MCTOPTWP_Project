from django.db import models


class BudgetValidation(models.Model):
    budget = models.IntegerField(null=False, blank=False)
    spendings = models.IntegerField(null=False, blank=False)
    sum_of_spendings = models.IntegerField(null=False, blank=False)
    is_validated = models.BooleanField(default=False)
