from PIL import Image
import re
import pytesseract

def get_info_bagel(image: str):
# Open the image using PIL
    img = Image.open(image)
    
    # Define a threshold for image binarization
    thresh = 200
    
    # Define a function to convert image to binary (black and white) using the threshold
    fn = lambda x: 255 if x > thresh else 0
    
    # Convert the image to a binary image (1-bit pixels, black and white)
    r = img.convert('L').point(fn, mode='1')
    width, height = img.size
    
    # Crop a portion of the image to extract the invoice number
    invoice_img = r.crop((0, height * 0.4, width * 0.175, height * 0.5))
    
    config = ('-l eng --oem 3 --psm 6')
    
    # Use Tesseract OCR to extract text from the invoice image
    invoice = pytesseract.image_to_string(invoice_img, config=config)
    
    invoice_pattern = r'(\d{6})'
    
    # Search for the invoice number in the extracted text
    match = re.search(invoice_pattern, invoice)
    
    if match:
        # If a match is found, use it as the invoice number
        invoice = match.group(1)
    else:
        # If no match is found, return None for both invoice and date
        return None, None
    
    # Crop a portion of the original image to extract the date
    date_img = img.crop((width * 0.20, height * 0.05, width * 0.45, height * 0.2))
    
    # Display the date image
    date_img.show()
    
    date_pattern = r'^(\d{2}/\d{2}/\d{2})$'
    
    while True:
        # Prompt the user to enter a date or 'Q' to quit and flag for review
        input_date = input("Enter a date (MM/DD/YY) or Press Q to quit and flag for review: ").strip()
        
        if re.match(date_pattern, input_date):
            return invoice, input_date
        else:
            if input_date.upper() == 'Q':
                # If 'Q' is entered, return None for both invoice and date
                return None, None
            print("Invalid Input")  # Notify the user of an invalid input