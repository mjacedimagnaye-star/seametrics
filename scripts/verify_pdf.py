import pypdf

reader = pypdf.PdfReader('paper/SeaMetrics_Final_Paper.pdf')
print(f"Total pages in generated PDF: {len(reader.pages)}")
for idx, page in enumerate(reader.pages):
    lines = [line.strip() for line in page.extract_text().splitlines() if line.strip()]
    first_line = lines[0] if lines else 'EMPTY'
    last_line = lines[-1] if lines else 'EMPTY'
    print(f"Page {idx+1}: {len(lines)} lines | First: '{first_line[:45]}' | Last: '{last_line[:45]}'")
