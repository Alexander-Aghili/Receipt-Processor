# Receipt Scanner with Tesseract OCR

This README provides an overview of a receipt scanner application that uses Tesseract OCR to extract information from scanned receipts. The application is designed to download scanned receipts from an email account, scan receipts from specific vendors (Pepsi, Sysco, Bimbo, Yerba, Peerless, UNFI, The Bagelry), extract the invoice number and date, rename the files, and forward them to another email address.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Prerequisites

Before using the Receipt Scanner, ensure that you have the following prerequisites in place:

- **Python**: You need to have Python installed on your system. This application is designed to work with Python 3.

- **Tesseract OCR**: Install Tesseract OCR on your system. You can download it from the [official website](https://github.com/tesseract-ocr/tesseract).

- **Email Account**: You need access to the email account from which the receipts will be downloaded and the email account to which you want to send the processed receipts.

- **Dependencies**: Install the required Python dependencies using `pip`:

  ```bash
  pip install pytesseract pillow imaplib smtplib
  ```

- **Email Libraries**: Depending on your email service provider, you may need to install additional libraries. For example, if you are using Gmail, you can install `google-auth`:

  ```bash
  pip install google-auth
  ```

## Installation

1. Clone the receipt processor repository to your local machine:

   ```bash
   git clone https://github.com/Alexander-Aghili/receipt_processor.git
   ```

2. Navigate to the project directory:

   ```bash
   cd receipt_processor
   ```


## Configuration

All regex to extract data is contained in regex_key.json

## Usage

To use the Receipt Scanner, follow these steps:

1. Run the application:

   ```bash
   python3 receipt_scanner.py
   ```

2. The application will log in to your source email account using an OAuth pop up, download the scanned receipts, scan them for specified vendors, extract invoice numbers and dates, rename the files, and send them to the destination email account.

3. If the program fails to find the invoice or date, it will ask you for input. After that, it will continue normally. The program currently doesn't verify validity of user input right now so carefully enter information.