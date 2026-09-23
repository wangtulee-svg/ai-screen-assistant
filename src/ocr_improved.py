"""
src/ocr_improved.py
OCR ທີ່ປັບປຸງແລ້ວ - ອ່ານຂໍ້ຄວາມໄດ້ຖືກຕ້ອງຂຶ້ນ
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import re


class ImprovedOCR:
    """OCR ທີ່ປັບປຸງແລ້ວ"""
    
    def __init__(self, lang="eng"):
        """ຕັ້ງຄ່າ"""
        self.lang = lang
        
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract Version: {version}")
        except Exception as e:
            print(f"⚠️ Tesseract Error: {e}")
    
    def preprocess_image(self, image):
        """
        ປັບປຸງຮູບພາບຢ່າງລະອຽດ
        """
        # ແປງເປັນ Grayscale
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # ປັບຂະໜາດໃຫຍ່ຂຶ້ນ
        h, w = gray.shape
        scale = 2.5
        resized = cv2.resize(gray, (int(w * scale), int(h * scale)), 
                             interpolation=cv2.INTER_CUBIC)
        
        # ຫຼຸດ noise
        denoised = cv2.fastNlMeansDenoising(resized, h=10)
        
        # ປັບ contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # ແປງເປັນ binary
        _, thresh = cv2.threshold(enhanced, 0, 255, 
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # ປັບໃຫ້ຕົວອັກສອນຊັດ
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.dilate(thresh, kernel, iterations=1)
        processed = cv2.erode(processed, kernel, iterations=1)
        
        return processed
    
    def extract_text(self, image, psm=6):
        """
        ອ່ານຂໍ້ຄວາມຈາກຮູບ
        
        Args:
            image: ຮູບພາບ
            psm: Page Segmentation Mode
                6 = ບັນທັດດຽວ
                4 = ຫຼາຍຖັນ
                3 = ອັດຕະໂນມັດ
        """
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        processed = self.preprocess_image(image)
        
        try:
            # ລອງຫຼາຍ PSM
            text = pytesseract.image_to_string(
                processed,
                lang=self.lang,
                config=f'--psm {psm} --oem 3'
            )
            return text.strip()
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return ""
    
    def extract_text_multi_psm(self, image):
        """
        ລອງຫຼາຍ PSM ແລ້ວເລືອກທີ່ດີທີ່ສຸດ
        """
        results = []
        
        for psm in [6, 4, 3]:
            text = self.extract_text(image, psm=psm)
            if text:
                results.append((psm, text, len(text)))
        
        if not results:
            return ""
        
        # ເລືອກທີ່ມີຂໍ້ຄວາມຫຼາຍທີ່ສຸດ
        best = max(results, key=lambda x: x[2])
        return best[1]
    
    def extract_structured_mcq(self, image):
        """
        ອ່ານ ແລະ ວິເຄາະ MCQ ແບບມີໂຄງສ້າງ
        """
        text = self.extract_text_multi_psm(image)
        
        if not text:
            return None
        
        # ແຍກບັນທັດ
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # ກັ່ນຕອງບັນທັດທີ່ບໍ່ຕ້ອງການ
        cleaned_lines = []
        for line in lines:
            # ຂ້າມບັນທັດທີ່ສັ້ນເກີນ
            if len(line) < 3:
                continue
            
            # ຂ້າມບັນທັດທີ່ມີຕົວອັກສອນພິເສດຫຼາຍ
            special = sum(1 for c in line if not c.isalnum() and c not in ' .,!?-()?:')
            if special > len(line) * 0.4:
                continue
            
            # ຂ້າມບັນທັດທີ່ເປັນພຽງເຄື່ອງໝາຍ
            if not any(c.isalnum() for c in line):
                continue
            
            cleaned_lines.append(line)
        
        # ຊອກຫາ MCQ
        question = None
        options = []
        
        for i, line in enumerate(cleaned_lines):
            # ຊອກຄຳຖາມ
            if question is None:
                if '?' in line:
                    question = line
                    continue
                if re.match(r'^(what|why|how|when|where|who|which)', line, re.I):
                    question = line
                    continue
            
            # ຊອກຕົວເລືອກ
            match = re.match(r'^([A-Da-d])[\.\)]\s*(.+)$', line)
            if match:
                opt_text = match.group(2).strip()
                # ກັ່ນຕອງ
                if len(opt_text) >= 1 and len(opt_text) <= 100:
                    options.append(opt_text)
        
        if question and len(options) >= 2:
            return {
                "question": question,
                "options": options[:4],
                "is_mcq": True
            }
        
        return None


def test_improved_ocr():
    """ທົດສອບ Improved OCR"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Improved OCR")
    print("=" * 60)
    
    ocr = ImprovedOCR()
    
    # ຊອກຫາຮູບພາບຫຼ້າສຸດ
    screenshots_dir = "data/screenshots"
    if not os.path.exists(screenshots_dir):
        print("❌ ບໍ່ມີໂຟນເດີ screenshots")
        return
    
    files = sorted([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
    if not files:
        print("❌ ບໍ່ມີຮູບພາບ")
        return
    
    latest = files[-1]
    filepath = os.path.join(screenshots_dir, latest)
    
    print(f"📸 ຮູບພາບ: {filepath}")
    
    # ອ່ານຮູບ
    image = cv2.imread(filepath)
    
    # ອ່ານຂໍ້ຄວາມ
    print("\n📝 ກຳລັງອ່ານຂໍ້ຄວາມ...")
    text = ocr.extract_text_multi_psm(image)
    
    print("\n" + "=" * 60)
    print("📝 ຂໍ້ຄວາມທີ່ອ່ານໄດ້:")
    print("=" * 60)
    print(text if text else "(ບໍ່ພົບ)")
    print("=" * 60)
    
    # ວິເຄາະ MCQ
    print("\n🔍 ກຳລັງວິເຄາະ MCQ...")
    mcq = ocr.extract_structured_mcq(image)
    
    if mcq:
        print("\n✅ ພົບ MCQ!")
        print(f"📝 ຄຳຖາມ: {mcq['question']}")
        print("📋 ຕົວເລືອກ:")
        for i, opt in enumerate(mcq['options']):
            print(f"   {chr(65+i)}. {opt}")
    else:
        print("\n⚠️ ບໍ່ພົບ MCQ")


if __name__ == "__main__":
    test_improved_ocr()