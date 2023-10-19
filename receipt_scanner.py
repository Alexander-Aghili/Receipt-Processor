from pdf_image import *
from pdf_scanner_bagel import *
from pdf_scanner_gen import *
from gmail import *
from PIL import Image
import glob, os
# Function to replace the dates with MM/DD/YYYY format and convert YY to YYYY
def replace_date(date_str):
    parts = date_str.split('/')

    if len(parts) < 3:
        return date_str
    
    # Check if the year is YY format, and convert it to YYYY format
    if len(parts[2]) == 2:
        parts[2] = '20' + parts[2]
    
    return '.'.join(parts)

def user_input():
    print("For all inputs enter nothing for default")
    user = input("Please provide your email: ")
    receipt_email = input("Please provide receipt email: ")
    to_user = input("Please provide email to send receipts")
    num_messages_str = input("How many recent emails would you like to collect receipts from: ")
    
    #Defaults
    if user == "":
        user="awaghili@ucsc.edu"
    if receipt_email == "":
        receipt_email = "zlaclair@ucsc.edu"
    if to_user == "":
        to_user = "zlaclair_ucsc.edu"
    try:
        num_messages= int(num_messages_str)
    except Exception:
        num_messages = 0


    return user, receipt_email, to_user, num_messages

def main():

    # Get user input
    user, receipt_email, to_user, num_messages = user_input()

    # Get messages from the sender
    get_messages_from_sender(num_messages, receipt_email)

    # Change the current working directory to the current directory
    os.chdir("./")

    # Iterate through PDF files in the current directory
    for file in glob.glob("*.pdf"):
        # Convert PDF to image
        image = convert_pdf_to_image(file)

        # Extract invoice and date information from the image
        invoice, date = get_info(image)

        # Check if invoice or date is missing
        if invoice is None or date is None:
            # Try to extract bagel-related information if not found in the initial extraction
            bagel_invoice, bagel_date = get_info_bagel(image)
            if bagel_invoice is None or bagel_date is None:
                # Display the image and prompt the user for missing information
                img = Image.open(image)
                img.show()
                if invoice is None:
                    invoice = input("Invoice Number: ")
                if date is None:
                    date = input("Date (MM/DD/YY): ")
            else:
                # Use bagel-related information if found
                invoice, date = bagel_invoice, bagel_date

        # Replace date format if needed
        date = replace_date(date)

        # Remove the original image file
        os.remove(image)

        # Create a new filename based on date and invoice number
        new_file_name = date + "-" + invoice + ".pdf"

        # Rename the PDF file
        os.rename(file, new_file_name)

    # Prompt the user to review the titles of the PDFs
    input("Review the titles of the pdfs and click any button when ready to send")

    # Send a message to the specified user
    send_message(to_user, user)

    # Remove all PDF files in the current directory
    for file in glob.glob("*.pdf"):
        os.remove(file)

            
if __name__ == "__main__":
    main()