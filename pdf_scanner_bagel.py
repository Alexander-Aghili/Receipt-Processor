from PIL import Image
import re
import pytesseract

def get_info_bagel(image: str):
    img = Image.open(image)
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    r = img.convert('L').point(fn, mode='1')
    width, height = img.size
    

    invoice_img = r.crop((0, height *.4, width *.175, height * .5))
    # Simple image to string
    
    config = ('-l eng --oem 3 --psm 6')
    invoice = pytesseract.image_to_string(invoice_img, config=config)
    invoice_pattern = r'(\d{6})'
    match = re.search(invoice_pattern, invoice)
    if match:
        invoice = match.group(1)
    else:
        return None, None

    
    date_img = img.crop((width*.20, height *.05, width * .45, height * .2))

    date_img.show()
    date_pattern = r'^(\d{2}/\d{2}/\d{2})$'
    while True:
            
        input_date = input("Enter a date (MM/DD/YY) or Press Q to quit and flag for review: ").strip()

        if re.match(date_pattern, input_date):
            return invoice, input_date
        else:
            if input_date.upper() == 'Q':
                return None, None
            print("Invalid Input")
