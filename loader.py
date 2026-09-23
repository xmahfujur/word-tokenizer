import pymupdf
from pathlib import Path

def load_pdf(file_path):
    with open('data.txt', 'w', encoding='utf-8') as f:
        
        dataset_directory = Path(file_path)

        for pdf_dir in dataset_directory.rglob('*.pdf'):
            print('Reading ', pdf_dir)
            pdf = pymupdf.open(pdf_dir)

            for page in pdf:
                f.write(page.get_text())
                f.write('\n\n')

            pdf.close()
