import docx

doc = docx.Document('paper/SeaMetrics_Final_Paper.docx')
print(f"Total paragraphs in DOCX: {len(doc.paragraphs)}")
print(f"Total tables in DOCX: {len(doc.tables)}")

table_summary = []
for idx, tbl in enumerate(doc.tables):
    rows = len(tbl.rows)
    cols = len(tbl.columns)
    first_cell = tbl.rows[0].cells[0].text.strip().replace('\n', ' ')
    table_summary.append(f"Table {idx+1}: {rows}x{cols} | First cell: '{first_cell[:30]}'")

for s in table_summary:
    print(s)

print(f"Page width: {doc.sections[0].page_width.inches} in")
print(f"Page height: {doc.sections[0].page_height.inches} in")
