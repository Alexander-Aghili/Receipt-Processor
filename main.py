from pdf_image import *
from pdf_scanner_bagel import *
from pdf_scanner_sysco import *
from gmail import *
from PIL import Image
import glob, os

# Function to replace the dates with MM/DD/YYYY format and convert YY to YYYY
def replace_date(match):
    date_str = match.group()
    parts = date_str.split('/')
    
    # Check if the year is YY format, and convert it to YYYY format
    if len(parts[2]) == 2:
        parts[2] = '20' + parts[2]
    
    return '.'.join(parts)

def main():

    get_messages_from_sender()
    return

    os.chdir("./")
    for file in glob.glob("*.pdf"):
        image = convert_pdf_to_image(file)
        invoice, date = get_info_sysco(image)
        if invoice is None or date is None:
            invoice, date = get_info_bagel(image)
            if invoice is None or date is None:
                img = Image.open(image)
                img.show()
                invoice = input("Invoice Number: ")
                date = input("Date (MM/DD/YY): ")
    
        date_pattern = r'(\d{2}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4})'

        date = re.sub(date_pattern, replace_date, date)
        os.remove(image)
        new_file_name = date + "-" + invoice + ".pdf"
        print(new_file_name)
        # os.rename(file, )
            
if __name__ == "__main__":
    main()