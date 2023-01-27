from docx import Document
from docx.shared import Inches

def createDocument(title, allRows):
    document = Document()
    document.add_heading(title, 1)
    for page in allRows:
        table = document.add_table(rows=0, cols=2)
        for row in page[0:]:
            row_cells = table.add_row().cells
            image = row_cells[0].paragraphs[0]
            text = row_cells[1].paragraphs[0]
            run = image.add_run()
            run.add_picture(row[0], width = Inches(1.75))
            text.add_run(row[1])
    document.save(title + '.docx')
