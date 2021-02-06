from django.contrib import admin

from .models import SavedReport


class SavedReportAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "date_created",
        "run_by",
    )
    raw_id_fields = ("run_by",)
    readonly_fields = ("run_by", "report")


admin.site.register(SavedReport, SavedReportAdmin)
