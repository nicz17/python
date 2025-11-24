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

    def newPage(self):
        """Adds an empty page."""
        self.pdf.add_page()

    def addTitle(self, title: str):
        """Adds a centered title."""
        self.pdf.set_font("Arial", size=18) # font and textsize
        self.pdf.cell(200, 10, txt=title, ln=1, align="C")

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

    def testFpdf(self):
        self.log.info('Testing FPDF')

        pdf = fpdf.FPDF(format='A4') #pdf format

        pdf.add_page() # create new page
        pdf.set_font("Arial", size=12) # font and textsize
        #self.log.info(f'Page width: {fpdf.epw}')

        # Title
        pdf.set_font("Arial", size=18) # font and textsize
        pdf.cell(200, 10, txt="Hello World", ln=1, align="C")

        # Body text
        pdf.set_font("Arial", size=12) # font and textsize
        pdf.cell(200, 10, txt="your text 1", ln=1, align="L")
        pdf.cell(200, 10, txt="your text 2", ln=1, align="C")
        pdf.cell(200, 10, txt="your text 3", ln=1, align="R")

        # Add an image
        image_path = "example.jpg"
        #pdf.image(image_path, x=10, y=50, w=100)
        pdf.image(image_path, x=55, w=100)
        pdf.cell(txt="Image legend", w=200, h=10, align="C")

        # Save
        filename = 'test.pdf'
        self.log.info(f'Saving PDF as {filename}')
        pdf.output(filename)
        pdf.close()

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
    doc.newPage()
    doc.addTitle('PDFDocument Test')
    doc.addText('Hello World!')
    doc.addImage('palettes/HeatPalette.png', 'Heat palette preview')
    doc.newPage()
    doc.addText('Second page')
    doc.save('test.pdf')

if __name__ == '__main__':
    testPdfDoc()