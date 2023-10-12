from PIL import Image
import re, json
import pytesseract

def check_for_info(text: str, data: map, type: str):

    # Define the regex pattern
    pattern = data[type + '_regex_invoice']

    # Search for the pattern in the text
    match = re.search(pattern, text)

    invoice_number = None
    # Check if a match is found
    if match:
        # Extract the second number (2nd capture group)
        invoice_number = match.group(1)


    pattern = data[type + '_regex_date']

    # Search for the pattern in the text
    match = re.search(pattern, text)

    date = None
    # Check if a match is found
    if match:
        # Extract the matched date
        date = match.group(1)

    return invoice_number, date

    

def get_info(image: str):
    # Simple image to string
    config = ('-l eng --oem 3 --psm 6')
    text = pytesseract.image_to_string(Image.open(image), config=config)
    
    f = open('./regex_key.json')
    data=json.load(f)

    keywords = data['get_type']

    pattern = re.compile(keywords, re.IGNORECASE)
    match = pattern.search(text)

    if match:
        print(match.group(0))
        return check_for_info(text, data, match.group(0).lower())
    
    print(image)
    return None, None

    