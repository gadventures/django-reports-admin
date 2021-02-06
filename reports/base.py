from collections import OrderedDict
from datetime import datetime
from typing import List
import csv
import io
import logging

from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.defaultfilters import title
from django.apps import apps
from django.conf import settings

from .models import SavedReport

logger = logging.getLogger(__name__)
EMPTY_DATA_XML = "<report/>"


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class ModelReport(object):
    """
    The base report which is inherited in each application that requires
    reporting. Using just this class will allow export of all fields
    in a model to CSV.

    Call tree:
        -> run_report
            -> collect_data
                -> get_row_data
                    -> get_field_lookups
                        -> get_model_fields
            -> generate_output
                -> as_csv
                    -> get_fields
            -> save | download

    The django admin calls this class, which re-instantiates this
    class to run the report. It's the circle of life.
    """

    # Name that appears in the admin action dropdown for generating the report
    name = "Report - Export Selected"

    # Fields to include or exclude from the model if the default
    # get_fields method is not overridden.
    include, exclude = [], []

    # For limiting the maximum number of records that can be reported on.
    # Useful for limiting the impact of large reports.
    max_records = None

    # If True, select_related() will be called on the queryset before
    # running the report. If only a small bit of data is being accessed
    # from a model, turning this off may result in smaller queries. For
    # reports that follow a lot of relationships, leave this on to get
    # faster report generation (at the expense of larger queries).
    select_related = True

    # See `get_fields`
    fields, field_lookups = [], []

    # The rows of data populated by `generate`
    data = []

    # A ModelReport can be populated by default, with a queryset. Although usage
    # within the admin will override this, it can be useful for testing within a
    # Python environment (shell/tests) to define this attribute
    queryset = None

    def __init__(self, *args, **kwargs):
        # Make the django admin shows a nice name...
        self.short_description = self.__name__ = self.name

        # These properties are populated when the class is called,
        # via the django admin (see __call__)
        self.user_id = kwargs.get("user_id")
        self.app_label = kwargs.get("app_label")
        self.model_name = kwargs.get("model_name")
        self.queryset = kwargs.get("queryset", self.queryset)

        # If the admin has not defined a query through __call__, use the defined
        # `queryset` attribute.
        if self.queryset is not None:
            self.query = self.queryset.query

            model = self.queryset.model
            self.model_name = model._meta.model_name
            self.app_label = model._meta.app_label

    def get_report_params(self, request, queryset):
        """
        Return the parameters that will be used to instantiate this report
        """
        model = queryset.model
        # Simplify the query to an id__in lookup. The queryset must
        # be evaluated via `list` to avoid pickling issues which is necessary
        # for running as a task.
        pks = list(queryset.values_list("pk", flat=True))
        queryset = model.objects.filter(pk__in=pks)

        # Create an instance of this class so we're threadsafe-ish
        # Use simple data structures so that it pickles nicely when
        # run as a task. It's better to pickle the QuerySet.query rather
        # than the entire QuerySet, as all of the data/rows would be evaluated
        # and passed to the task (bad news bears); `get_queryset` recreates the
        # full queryset when the report runs.
        params = {
            "report_class": self.__class__,
            "user_id": request.user.id,
            "queryset": queryset,
            "app_label": model._meta.app_label,
            "model_name": model._meta.object_name,
        }
        return params

    def __call__(self, model_admin, request, queryset, **kwargs):
        """
        This class is callable and matches the Django action parameters
        so that it can be added as an action itself.

        `model_admin`
            Instance of the model's ModelAdmin
        `request`
            The HTTP request
        `queryset`
            Model queryset; typically contains the objects selected in the admin
        """
        if self.max_records and queryset.count() > self.max_records:
            model_admin.message_user(
                request, "This report is limited to %s records." % self.max_records
            )
            return False

        # Bind request so we're not passing it around through various hook functions
        self.request = request

        params = self.get_report_params(request, queryset)
        report = self.__class__(**params)

        try:
            saved_report = report.run_report()
        except Exception as exc:
            logger.error("Failed to run report", exc_info=True)
            self.send_error_notification(model_admin)
            return
        else:
            self.send_success_notification(model_admin, saved_report=saved_report)

        return saved_report

    def run_report(self) -> SavedReport:
        """
        Default method responsible for generating the output of this report.
        """
        self.collect_data()
        output = self.generate_output()
        saved_report = self.save(output)
        return saved_report

    def send_error_notification(self, model_admin):
        """
        Hook to deliver a notification of failed report compilation
        """
        model_admin.message_user(
            self.request,
            "Your report could not be compiled. Please check the error logs or contact your administrator.",
        )

    def send_success_notification(self, model_admin, saved_report=None):
        """
        Hook to deliver a notification of success when a report has been saved.
        """
        if saved_report is None:
            return
        model_admin.message_user(
            self.request,
            "Your report has completed and is available within the <em>{0}</em> section of the admin. Or, you can download it directly <a href='{1}'>here</a>".format(
                apps.get_app_config("reports").verbose_name,
                saved_report.report_file.url,
            ),
            extra_tags="safe",
        )

    def collect_data(self) -> List[OrderedDict]:
        """
        Collect the rows of data for the report
        """
        self.data = []  # Clear existing data
        for obj in self.get_queryset():
            self.data.append(self.get_row_data(obj))
        return self.data

    def get_row_data(self, obj):
        """
        Collect a single row of data from the given `obj`. By default, the data
        will be collected from the configuration returned by get_field_lookups.
        This is a good method to override for custom data collection.

        `obj`
            A data object from the `objects` list passed to generate()
        """
        data = OrderedDict()
        field_lookups = self.get_field_lookups()
        for field, value in field_lookups:
            # Send the object to any callable
            if callable(value):
                data[field] = value(obj)
            # Check if it's a named property or callable on the object
            elif hasattr(obj, value):
                val = getattr(obj, value)
                data[field] = val() if callable(val) else val
            else:
                data[field] = value
        return data

    def generate_output(self) -> io.StringIO:
        """
        By default generates and returns CSV output.
        """
        return self.as_csv()

    def get_model(self):
        return apps.get_model(self.app_label, self.model_name)

    def get_queryset(self):
        """
        Create a queryset from the Query
        """
        qs = self.get_model().objects.all()
        qs.query = self.query
        if self.select_related:
            qs = qs.select_related()
        return qs

    def get_user(self):
        if self.user_id is None:
            return
        return User.objects.get(id=self.user_id)

    def get_user_email(self):
        """
        By default, attempt to fetch email of active admin user, otherwise
        fallback to use settings.ADMINS
        """
        try:
            return self.get_user().email
        except User.DoesNotExist:
            logger.warning("User not set for report notification")
            return [email for name, email in settings.ADMINS]

    def save(self, output) -> SavedReport:
        """
        Save the report to disk

        `notify`
            Send an email to the user notifying them that their report
            is complete.
        """
        user = self.get_user()
        saved = SavedReport.objects.create(report=self.name, run_by=user)
        saved.save_file(output, self.get_filename())
        return saved

    def get_filename(self):
        """
        Return the filename for saving or downloading
        """
        return "{0}-{1}.csv".format(slugify(self.name), str(datetime.now()))

    def get_fields(self):
        """
        Return a flat list of the field names which _may_ exist in the
        generated data.
        """
        if self.fields:
            return self.fields
        # For a fixed set of field lookups, we can ascertain the fields from
        # the first element in each tuple.
        elif self.field_lookups:
            self.fields = [k for k, v in self.field_lookups]
        # If data is already collected, get the fields from the data instead of
        # the model.
        elif self.data:
            self.fields = self._get_data_fields()
        else:
            self.fields = self._get_model_fields()
        return self.fields

    def get_field_lookups(self):
        """
        Returns a list of column name-value/callback tuples. Any callable
        value will be passed the instance of the object being evaluated during
        data collection. By default, ALL fields from the model will be included.

        e.g.
            [
                # Static value
                # Note, if the string is a property of the object,
                # that will take precidence.
                ('Column Name', 'Value'),

                # Callback to a method on the ModelReport
                ('Example 2', self.my_callback),

                # Inline lambda callback
                ('Example 3', lambda obj: unicode(obj.my_method())),

                # Attempt to get the property from the object by name
                ('Example 4', 'property_name'),
            ]
        """
        if self.field_lookups:
            return self.field_lookups
        self.field_lookups = [
            (title(field), field) for field in self._get_model_fields()
        ]
        return self.field_lookups

    def as_csv(self) -> io.StringIO:
        """
        Return report as a string of comma separated values
        """
        if not self.data:
            logger.warning("Data is empty. Call collect_data before exporting output.")
            return ""

        fields = self.get_fields()
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow(self.fields)
        for row in self.data:
            try:
                csv_writer.writerow([row.get(k, "") for k in fields])
            except Exception:
                logger.error("Failed to write row %s", row, exc_info=True)
        return output.getvalue()

    def _get_model_fields(self):
        """
        Retrieve fields from the model definition
        """
        ct = ContentType.objects.get_for_model(self.get_model())
        opts = ct.model_class()._meta
        return [field.name for field in opts.fields]

    def _get_data_fields(self):
        """
        Analyzes the collected data and returns the field names available.
        """
        fieldnames = []

        # Straight up dict
        if isinstance(self.data, dict):
            fieldnames = self.data.keys()
        # Do we have a list of dicts?
        elif isinstance(self.data, list):
            fieldnames = []
            # It's possible that each dict in the list has different
            # keys, so we get a set of all keys to use for the header row.
            # A real `set` object isn't used because we want to retain order
            # wherever possible.
            for d in self.data:
                for k in d.keys():
                    if k not in fieldnames:
                        fieldnames.append(k)
        return fieldnames


class Reports(object):
    """
    For registering Models with reports
    """

    report_module_name = "report"
    # Stores the reports registered with various models
    _models = {}

    def __init__(self, *args, **kwargs):
        self._models = {}

    def register(self, model, report_class=None, **kwargs):
        """
        `model`
            The model for which the report can be run. If None, the report
            will be available for ALL models (global action).

        `report_class`
            The class that will be instantiated for running the report via
            it's `run_report` method. Should inherit from ModelReport.
        """
        logger.debug("Reports.register: %s %s" % (model, report_class))
        if not report_class:
            report_class = ModelReport

        # Instantiate the report class to save in the registry
        if model in self._models:
            self._models[model].append(report_class())
        else:
            self._models[model] = [report_class()]

    def _get_registry(self):
        registry = self._models.copy()
        return registry

    registry = property(_get_registry)

    def discover(self):
        """
        Discover INSTALLED_APPS reports.py modules and fail silently when
        not present. This forces an import on them to register any report
        configuration.

        This should be called in a place that's loaded once. It is recommended
        this lives within an AppConfig, e.g.

        class ReportConfig(AppConfig):

            def ready(self):
                from .base import reports
                reports.discover()
        """
        from importlib import import_module
        from django.conf import settings
        from django.utils.module_loading import module_has_submodule

        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            # Attempt to import the app's admin module.
            try:
                import_module("%s.%s" % (app, self.report_module_name))
                logger.debug("Importing %s from %s" % (self.report_module_name, app))
            except:
                # Decide whether to bubble up this error. If the app just
                # doesn't have a reports module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, self.report_module_name):
                    raise

        self._add_actions()

    def _add_actions(self):
        """
        Register the actions for each model
        """
        from django.contrib import admin

        for model, model_admin in admin.site._registry.items():
            if model not in self.registry:
                continue

            # It seems that if the model_admin class doesn't explicitly set an
            # `actions` property, the action will be added on the super class,
            # thus appearing everywhere. So make sure there is a specific class
            # based property set.
            if not model_admin.__class__.actions:
                model_admin.__class__.actions = []

            # Django finds actions on the class, not the instance, so
            # add actions to the class definition.
            for report in self.registry[model]:
                actions = model_admin.__class__.actions
                if isinstance(actions, list):
                    actions.append(report)
                elif isinstance(actions, tuple):
                    model_admin.__class__.actions = actions + (report,)
                else:
                    logger.error(
                        "Unexpected type for ModelAdmin actions when registering %s",
                        report.name,
                    )
                    continue

        # Add any global actions (not associated with a specific model)
        for report in self.registry.get(None, []):
            logger.info("Add %s globally" % (report,))
            admin.site.add_action(report)


class XMLModelReport(ModelReport):
    """
    Saves output as XML instead of CSV using huTools dict2xml/list2xml
    """

    def generate_output(self):
        return self.as_xml()

    def as_xml(self):
        """
        Return the data as an XML object
        """
        if not self.data:
            logger.warning("Data is empty. Call collect_data before exporting output.")
            return EMPTY_DATA_XML

        try:
            from huTools.structured import dict2xml
            from huTools.structured import list2xml
        except ImportError:
            logger.error("Report.as_xml could not run. Requires huTools.")
            return EMPTY_DATA_XML

        if isinstance(self.data, dict):
            return dict2xml(self.data, roottag="report")
        elif isinstance(self.data, list):
            return list2xml(self.data, root="report", elementname="item")
        else:
            raise Exception("Data must be a list or dict")


reports = Reports()
