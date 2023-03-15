from docx import Document
from docx.shared import Inches
from docx.shared import Pt


def create_document(title, all_rows, folder_selected, font_style, font_size, watermark_image, watermark_text):
    document = Document()
    style = document.styles['Normal']
    font = style.font
    font.name = font_style
    font.size = Pt(font_size)
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = 1.5
    section = document.sections[0]
    header = section.header
    footer = section.footer

    paragraph = header.paragraphs[0]
    paragraph.alignment = 1
    run = paragraph.add_run()
    run.add_text(title)
    paragraph = footer.paragraphs[0]
    paragraph.alignment = 1
    run = paragraph.add_run()
    run.add_text(watermark_text)
    run.add_text("   ")
    run.add_picture(watermark_image, width=Inches(0.20), height=Inches(0.20))

    for page in all_rows:
        table = document.add_table(rows=0, cols=2)
        for row in page[1:]:
            row_cells = table.add_row().cells
            image = row_cells[0].paragraphs[0]
            text = row_cells[1].paragraphs[0]
            run = image.add_run()
            run.add_picture(row[0], width=Inches(1.80), height=Inches(1.80))
            sentence = row.split()
            for word in sentence:

                if word:
                    text.add_run(word).bold = True
                else:
                    text.add_run(word)
            text.add_run(row[1])

    document.save(folder_selected + "/" + title + '.docx')
