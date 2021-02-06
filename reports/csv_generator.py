import csv
import io
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class CSVGenerator(object):
    """
    Utility for generating CSV output from a dictionary of fields with
    callables or values. Note, the order of fields will only be preserved if
    the `fields` dictionary is an OrderedDict.

    >>> def a_method(obj):
    >>>     return str(obj)
    >>> generator = CSVGenerator(fields={
            "Field 1": "Hard coded value",
            "Field 2": lambda o: str(o),
            "Field 3": a_method,
       })
    >>> output = generator.generate(objects=["list", "of", "data", "objects"])
    """
    def __init__(self, fields):
        self.fields = OrderedDict(fields)

    def generate(self, objects):
        """
        `objects`
            The list of objects from which to generate the report
        """
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow(self.fields)
        for obj in objects:
            data = self.get_row_data(obj)
            csv_writer.writerow([data[k] for k in self.fields.keys()])
        return output.getvalue()

    def get_row_data(self, obj):
        """
        Override this in the subclasses to create useful data

        `obj`
            A data object from the `objects` list passed to generate()
        """
        data = OrderedDict()
        for field, value in self.fields.items():
            if callable(value):
                data[field] = value(obj)
            # Check if it"s a named property or callable on the object
            elif hasattr(obj, value):
                val = getattr(obj, value)
                data[field] = val() if callable(val) else val
            else:
                data[field] = value
        return data
