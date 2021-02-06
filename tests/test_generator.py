from collections import OrderedDict
from django.test import TestCase

from reports.csv_generator import CSVGenerator


class CSVGeneratorTest(TestCase):
    def test_generate(self):
        """
        Test the generate method using ordered fields
        """

        def a_method(obj):
            return str(obj)

        # Use an ordered dict so the output is predictable
        fields = OrderedDict(
            [
                ("Field 1", "1"),  # Hard coded value
                ("Field 2", lambda o: str(o)),  # callable
                ("Field 3", a_method),  # callable
            ]
        )
        generator = CSVGenerator(fields=fields)
        output = generator.generate(
            objects=[
                "data",
                "data",
            ]
        )

        expected_output = u"Field 1,Field 2,Field 3\r\n1,data,data\r\n1,data,data\r\n"

        assert output == expected_output
