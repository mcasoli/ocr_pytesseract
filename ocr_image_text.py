# pip install pytesseract opencv-python
# https://github.com/UB-Mannheim/tesseract/wiki

import pyautogui as py

import cv2, os
import pytesseract
from pytesseract import Output


pytesseract_path = os.path.expandvars(r"%userprofile%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")  # Tesseract.exe
image_path = f"./img/screenshot"


class ocr_image_text:
    def __init__(self, pytesseract_path, image_path):
        self.pytesseract_path = pytesseract_path
        self.img_path = image_path


    def get_text_from_image(self, img_file: str | None = None):
         # Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = self.pytesseract_path

        if not img_file:
            img_file = '\ocr_capturedscreen.png'
            py.screenshot().save(f'{self.img_path}{img_file}')

        image = cv2.imread(f"{self.img_path}\{img_file}") 
        if image is None: # Valid image file
            raise ValueError(f"Não foi possível carregar a imagem em: {self.img_path}")

        # OCR image
        extracted_text = pytesseract.image_to_string(image, lang='por', config='--psm 6')

        print(extracted_text)
        return extracted_text

    def seach_text_in_image(self, text, image: str | None = None):
        if not image:
            captured_img = f'{self.img_path}\ocr_capturedscreen.png'
            py.screenshot().save(captured_img)

        image = cv2.imread(captured_img) 
        if image is None: # Valid image file
            raise ValueError(f"Não foi possível carregar a imagem em: {self.img_path}")
        
        # Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = self.pytesseract_path

        # OCR image
        d = pytesseract.image_to_data(image, output_type=Output.DICT, lang='por', config='--psm 6')

        # Search text in image
        for _i in range(len(d['text'])):
            if d['text'][_i].lower() == text.lower():
                # Get coordinates
                pX, pY, w, h = d['left'][_i], d['top'][_i], d['width'][_i], d['height'][_i]
                
                print(f"Found {text}: x={pX}, y={pY}, w={w}, h={h}")
                position_text = pX+w/2, pY+h/2
                
                return position_text
        else:
            print(f"Text {text} not found.")
            return

    def capture_img_part_screen(self, iX=100, iY=150, iW=400, iH=300):
        screenshot_part = f'{self.img_path}\screenshot_part.png'
        py.screenshot(region=(iX, iY, iW, iH)).save(screenshot_part)

        return screenshot_part



ocr = ocr_image_text(pytesseract_path, image_path) # Instance


extracted_text = ocr.get_text_from_image() # Get text

position_text = ocr.seach_text_in_image('') # Search position text in screen
if position_text:
    py.click(position_text) # click text
