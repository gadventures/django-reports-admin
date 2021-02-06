from django.db import models


class ReportTestModel(models.Model):
    """
    Used by ModelReport tests to test generation.
    """

    name = models.CharField(max_length=55)

    class Meta:
        app_label = "testapp"
