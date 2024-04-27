from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QTextDocument


class ToPDFConverter:
    def __init__(self):
        self.lines = []
        self.pdf_printer = QPrinter()
        self.pdf_printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        self.doc = QTextDocument()

    def set_lines(self, lines):
        self.lines = lines
        self.doc.setHtml("".join(self.lines))

    def save_as_pdf(self, path):
        self.pdf_printer.setOutputFileName(path)
        self.doc.print(self.pdf_printer)
