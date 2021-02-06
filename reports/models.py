from django.conf import settings
from django.db import models
from django.urls import reverse

REPORTS_FOLDER = getattr(settings, 'REPORTS_FOLDER', 'reports')


class SavedReport(models.Model):
    """
    Contains instances of saved reports, and ensures they are written to a file.
    """
    report = models.CharField(max_length=255, null=True, blank=False)
    run_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    report_file = models.FileField(upload_to=REPORTS_FOLDER)

    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('admin:reports_savedreport_change', args=[self.id])

    def save_file(self, content, filename):
        from django.core.files.base import ContentFile
        f = ContentFile(content)
        f.name = filename
        self.report_file = f
        self.save()
