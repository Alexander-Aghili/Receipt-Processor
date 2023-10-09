from pdf2image import convert_from_path

def convert_pdf_to_image(pdf):
    pages = convert_from_path(pdf, 350)
    image_name = pdf[0:8] + ".jpg"  
    pages[0].save(image_name, "JPEG")    
    return image_name 
