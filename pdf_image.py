from pdf2image import convert_from_path

pdfs = r"0005_001.pdf"
pages = convert_from_path(pdfs, 350)

i = 1
for page in pages:
    image_name = pdfs[0:8] + ".jpg"  
    page.save(image_name, "JPEG")
    i = i+1        
