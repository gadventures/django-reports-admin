from collections import OrderedDict
from django.test import TestCase

from reports.base import ModelReport

from .testapp.models import ReportTestModel


class ModelReportTest(TestCase):
    def test_collect_data(self):
        """
        Should return data based on input queryset
        """

        class FooReport(ModelReport):
            queryset = ReportTestModel.objects.all()

        ReportTestModel.objects.create(name="Name 1")
        ReportTestModel.objects.create(name="Name 2")

        report = FooReport()
        assert report.collect_data() == [
            OrderedDict(
                [
                    ("Id", 1),
                    ("Name", "Name 1"),
                ]
            ),
            OrderedDict(
                [
                    ("Id", 2),
                    ("Name", "Name 2"),
                ]
            ),
        ]
