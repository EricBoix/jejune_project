class PageLayout:
    """
    reader_page_number: str
        The page number as it appears to a human reader on the printed (or
        rendered by a pdf viewer) page. Note that, some pages might have roman
        numbering, some pages an integerand some pages may have no numbering
        at all (e.g. the cover or back-cover or some illustrative pages).
    """

    def __init__(self, reader_page_number, page_number):
        self._reader_page_number = reader_page_number
        self._page_number = page_number
        self._reference_text = "DUMMY UNDEFINED VALUE"

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._reader_page_number = self._reader_page_number
        result._page_number = self._page_number
        result._reference_text = self._reference_text
        return result

    @property
    def reader_page_number(self):
        return self._reader_page_number

    @property
    def page_number(self):
        return self._page_number

    @property
    def reference_text(self):
        return self._reference_text

    def set_reference_text(self, value):
        self._reference_text = value
