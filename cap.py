import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
data = pytesseract.image_to_string("captcha.png", lang='eng',config='--psm 13')
print(data)