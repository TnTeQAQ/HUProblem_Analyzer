import os
from utils.pdftools import PDF

pdf_path = 'pdf/'

result = os.listdir(pdf_path)

all_pdf = []

for file in result:
    print(pdf_path+file)
    all_pdf.append(PDF(pdf_path+file))

print(123)
print(123)