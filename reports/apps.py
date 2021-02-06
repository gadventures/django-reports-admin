from django.apps import AppConfig


class ReportConfig(AppConfig):
    name = "reports"
    verbose_name = "Django Model Reports"

    def ready(self):
        from .base import reports

        reports.discover()
