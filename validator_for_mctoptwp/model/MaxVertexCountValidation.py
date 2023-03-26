from django.db import models


class MaxVertexCountValidation(models.Model):
    sums_of_vertices = models.CharField(max_length=400)
    max_allowed_vertices_for_type_z = models.CharField(max_length=400)
    is_validated = models.BooleanField(default=False)
