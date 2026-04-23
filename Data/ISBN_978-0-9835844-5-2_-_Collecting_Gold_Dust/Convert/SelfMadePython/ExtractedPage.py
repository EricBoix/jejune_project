from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)
        self.removed_header = None

    def set_removed_header(self, removed_header):
        self.removed_header = removed_header

    def __repr__(self):
        result = ExtractedPageBase.__repr__(self) + "\n"
        if self.removed_header is not None:
            result += "Removed header: " + repr(self.removed_header)
        return result
