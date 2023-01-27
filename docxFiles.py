from docx import Document
from docx.shared import Inches

def createDocument(title, allRows):
    document = Document()
    document.add_heading('title', 0)
    for page in allRows:
        document.add_heading('Page ' + str(page[0]), level=1)
        for row in page[1:]:
            document.add_heading(row[0], level=2)
            document.add_paragraph(row[1])
    document.save(title + '.docx')
