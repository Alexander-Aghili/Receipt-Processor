from PIL import Image
import re
import pytesseract

img = Image.open('0005_001.jpg')
thresh = 200
fn = lambda x : 255 if x > thresh else 0
r = img.convert('L').point(fn, mode='1')
width, height = img.size
r = r.crop((0, 0, width / 2, height * .55))
r.save('foo.jpg')
# Simple image to string
text = pytesseract.image_to_string(r)

print(text)