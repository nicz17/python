#!/usr/bin/env python3

import fpdf
import logging
import os


class PdfDoc:
    """Simple PDF document writer using fpdf."""
    # cf https://coderivers.org/blog/fpdf-python/
    # cf https://www.fpdf.org/en/doc/index.php
    log = logging.getLogger('PdfDoc')

    def __init__(self):
        """Constructor, creates an empty A4 PDF."""
        self.log.info('Welcome to PdfDoc')
        self.pdf = fpdf.FPDF(format='A4')
        self.newPage()

    def newPage(self):
        """Adds an empty page."""
        self.pdf.add_page()

    def addTitle(self, title: str):
        """Adds a centered title."""
        self.pdf.set_font("Arial", size=18) # font and textsize
        self.pdf.cell(200, 10, txt=title, ln=1, align="C")
        self.pdf.set_font("Arial", size=12) # back to normal font

    def addText(self, text: str):
        """Adds text."""
        self.pdf.set_font("Arial", size=12) # font and textsize
        self.pdf.cell(200, 10, txt=text, ln=1, align="C")

    def addImage(self, imgfile: str, legend: str):
        """Adds an image with an optional legend."""
        if not os.path.exists(imgfile):
            self.log.error(f'Image to add does not exist: {imgfile}')
            return
        
        self.pdf.image(imgfile, x=23, w=160)
        if legend:
            self.pdf.cell(txt=legend, w=200, h=10, align="C")

    def save(self, filename: str):
        """Saves the PDF to file."""
        self.log.info(f'Saving PDF as {filename}')
        self.pdf.output(filename)
        self.pdf.close()

def configureLogging():
    """Configures logging to have timestamped logs at INFO level on stdout."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('pdfWriter')

def testPdfDoc():
    """Simple test case for creating a PDF document."""
    configureLogging()
    doc = PdfDoc()
    doc.addTitle('PDFDocument Test')
    doc.addText('Hello World!')
    doc.addImage('palettes/HeatPalette.png', 'Heat palette preview')
    doc.newPage()
    doc.addText('Second page')
    doc.save('test.pdf')

if __name__ == '__main__':
    testPdfDoc()