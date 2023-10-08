from PIL import Image
import re
import pytesseract

# Simple image to string
text = pytesseract.image_to_string(Image.open('0007_001.jpg'))

# Define the regex pattern
pattern = r'\d{6}\s+(\d{9})'

# Search for the pattern in the text
match = re.search(pattern, text)

# Check if a match is found
if match:
    # Extract the second number (2nd capture group)
    invoice_number = match.group(1)
    print("Extracted Invoice Number:", invoice_number)
else:
    print("Invoice Number not found in the text.")


pattern = r'\b(\d{1,2}/\d{1,2}/\d{2}(\d{2})?)\b'

# Search for the pattern in the text
match = re.search(pattern, text)

# Check if a match is found
if match:
    # Extract the matched date
    date = match.group(1)
    print("Extracted Date:", date)
else:
    print("Date not found in the text.")
