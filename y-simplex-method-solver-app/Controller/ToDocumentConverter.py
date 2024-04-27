import pypandoc


class ToDocumentConverter:
    def __init__(self):
        self.lines = []

    def set_lines(self, lines):
        self.lines = lines

    def save_as_document(self, path):
        pypandoc.convert_text("\n".join(self.lines), "docx", format='html', outputfile=path)
