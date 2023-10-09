from pdf_scanner_bagel import *
from pdf_image import *
import os, glob

os.chdir("./")

for file in glob.glob("*.pdf"):
    print(file + " " + get_info_bagel(convert_pdf_to_image(file)))