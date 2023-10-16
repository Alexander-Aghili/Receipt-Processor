from pdf_image import *
from pdf_scanner_bagel import *
from pdf_scanner_gen import *
from gmail import *
from PIL import Image
import glob, os
# Function to replace the dates with MM/DD/YYYY format and convert YY to YYYY
def replace_date(date_str):
    parts = date_str.split('/')
    
    # Check if the year is YY format, and convert it to YYYY format
    if len(parts[2]) == 2:
        parts[2] = '20' + parts[2]
    
    return '.'.join(parts)

def user_input():
    # user = input("Please provide your email: ")
    # receipt_email = input("Please provide receipt email: ")
    user = "awaghili@ucsc.edu"
    receipt_email="zlaclair@ucsc.edu"
    num_messages = int(input("How many recent emails would you like to collect receipts from: "))
    
    return user, receipt_email, num_messages

def main():

    user, receipt_email, num_messages = user_input()
    get_messages_from_sender(num_messages, receipt_email)

    os.chdir("./")
    for file in glob.glob("*.pdf"):
        image = convert_pdf_to_image(file)
        invoice, date = get_info(image)
        if invoice is None or date is None:
            bagel_invoice, bagel_date = get_info_bagel(image)
            if bagel_invoice is None or bagel_date is None:
                img = Image.open(image)
                img.show()
                if invoice is None:
                    invoice = input("Invoice Number: ")
                if date is None:
                    date = input("Date (MM/DD/YY): ")
            else:
                invoice, date = bagel_invoice, bagel_date
                
        date = replace_date(date)
        os.remove(image)
        new_file_name = date + "-" + invoice + ".pdf"
        os.rename(file, new_file_name)

    input("Review the titles of the pdfs and click any button when ready to send")

    send_message()

    for file in glob.glob("*.pdf"):
        os.remove(file)

            
if __name__ == "__main__":
    main()