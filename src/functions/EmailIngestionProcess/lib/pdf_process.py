import base64
import io
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_pages(pdf_bytes):
    """
    Découpe un PDF en pages individuelles.
    Retourne une liste de bytes PDF.
    """
    pages = []
    reader = PdfReader(io.BytesIO(pdf_bytes))

    for i in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        output_stream = io.BytesIO()
        writer.write(output_stream)
        pages.append(output_stream.getvalue())

    return pages


def get_pages(pdf_bytes):

    pages_bytes = split_pdf_pages(pdf_bytes)

    pages_base64 = [
        base64.b64encode(page).decode("utf-8")
        for page in pages_bytes
    ]

    return pages_base64
