from django.contrib import admin

from reports.models import SavedReport


class SavedReportAdmin(admin.ModelAdmin):
    list_display = ('report', 'created', 'run_by',)
    raw_id_fields = ('run_by',)
    readonly_fields = ('run_by', 'report')

admin.site.register(SavedReport, SavedReportAdmin)
