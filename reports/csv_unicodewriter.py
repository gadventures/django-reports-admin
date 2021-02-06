import codecs
import csv
import io

from django.utils.encoding import smart_text


class CSVUnicodeWriter(object):
    # Derived from http://djangosnippets.org/snippets/993/
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a buffer
        self.buffer = io.StringIO()
        self.writer = csv.writer(self.buffer, dialect=dialect, **kwds)
        self.stream = f

        # Force BOM
        if encoding == "utf-16":
            f.write(str(codecs.BOM_UTF16))

        self.encoding = encoding

    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([smart_text(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the buffer ...
        data = self.buffer.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)

        # strip BOM
        if self.encoding == "utf-16":
            data = data[2:]

        # write to the target stream
        self.stream.write(data)
        # empty buffer
        self.buffer.truncate(0)
