class TextExtractor:
    """
    Pre-extracts text from all PDF pages before chapter breaking begins.
    This separates the text extraction concern from DocumentBreaker.
    """

    def __init__(self, reader, structural_info):
        self.reader = reader
        self.structural_info = structural_info

    def extract_all(self) -> dict[int, str]:
        """
        Extract text from all pages.
        Returns a dict mapping page_number to extracted text.
        """
        extracted_texts = {}
        for page_number in range(self.structural_info.total_page_number):
            if self.structural_info._page_is_dropped(page_number):
                continue
            original_page = self.reader.pages[page_number]
            try:
                text = original_page.extract_text(extraction_mode="layout")
            except NotImplementedError:
                # Fallback for PDFs with filter arrays that pypdf can't handle
                # in layout mode
                text = original_page.extract_text()
            # Normalize tabs to spaces (some PDFs have tabs instead of spaces)
            text = text.replace("\t", " ")
            # lstrip is required before holds_new_chapter classification
            extracted_texts[page_number] = text.lstrip()
        return extracted_texts
