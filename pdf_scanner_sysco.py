from PIL import Image
import re
import pytesseract

def get_info_sysco(image: str):
    # Simple image to string
    config = ('-l eng --oem 3 --psm 6')
    text = pytesseract.image_to_string(Image.open(image), config=config)
    
    # Define the regex pattern
    pattern = r'\d{6}\s+(\d{9})'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    invoice_number = None
    # Check if a match is found
    if match:
        # Extract the second number (2nd capture group)
        invoice_number = match.group(1)


    pattern = r'\b(\d{1,2}/\d{1,2}/\d{2}(\d{2})?)\b'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    date = None
    # Check if a match is found
    if match:
        # Extract the matched date
        date = match.group(1)

    return invoice_number, date
