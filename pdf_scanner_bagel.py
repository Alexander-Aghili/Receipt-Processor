from PIL import Image
import re
import pytesseract

def get_info_bagel(image: str):
    img = Image.open(image)
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    r = img.convert('L').point(fn, mode='1')
    width, height = img.size
    invoice_img = r.crop((0, height *.45, width / 5, height * .55))
    # Simple image to string
    config = ('-l eng --oem 3 --psm 3')
    invoice = pytesseract.image_to_string(invoice_img, config=config)

    date_img = img.crop((width*.20, height *.05, width * .45, height * .2))

    date_img.show()
    date_pattern = r'^(\d{2}/\d{2}/\d{2})$'
    while True:
            
        input_date = input("Enter a date (MM/DD/YY) or Press Q to quit and flag for review: ").strip()

        if re.match(date_pattern, input_date):
            return invoice.strip(), input_date
        else:
            if input_date == 'Q':
                return None, None
