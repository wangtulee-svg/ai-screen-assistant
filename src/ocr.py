"""
src/ocr.py
OCR ສຳລັບອ່ານຂໍ້ຄວາມຈາກຮູບພາບ
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os


class OCRReader:
    """ອ່ານຂໍ້ຄວາມຈາກຮູບພາບດ້ວຍ Tesseract"""
    
    def __init__(self, lang="eng+lao"):
        """
        ຕັ້ງຄ່າ OCR
        
        Args:
            lang: ພາສາທີ່ຈະອ່ານ (eng, lao, tha, ...)
        """
        self.lang = lang
        
        # ກວດສອບ Tesseract
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract Version: {version}")
        except Exception as e:
            print(f"⚠️ Tesseract not found: {e}")
            print("   ຕິດຕັ້ງ Tesseract ຈາກ: https://github.com/UB-Mannheim/tesseract/wiki")
    
    def preprocess_image(self, image):
        """
        ປັບປຸງຄຸນນະພາບຮູບພາບກ່ອນ OCR
        
        Args:
            image: ຮູບພາບ (numpy array)
        
        Returns:
            np.ndarray: ຮູບພາບທີ່ປັບປຸງແລ້ວ
        """
        # ແປງເປັນ Grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # ປັບຄວາມຄົມຊັດ
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # ຫຼຸດສິ່ງລົບກວນ
        denoised = cv2.fastNlMeansDenoising(enhanced, h=30)
        
        # ເພີ່ມຄວາມຄົມຊັດອີກຄັ້ງ
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text(self, image, preprocess=True):
        """
        ສະກັດຂໍ້ຄວາມຈາກຮູບພາບ
        
        Args:
            image: ຮູບພາບ (numpy array ຫຼື PIL Image)
            preprocess: ປັບປຸງຮູບກ່ອນ OCR ຫຼືບໍ່
        
        Returns:
            str: ຂໍ້ຄວາມທີ່ອ່ານໄດ້
        """
        # ແປງເປັນ numpy array ຖ້າເປັນ PIL Image
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # ປັບປຸງຮູບ
        if preprocess:
            processed = self.preprocess_image(image)
        else:
            processed = image
        
        # OCR
        try:
            # ໃຊ້ Tesseract
            text = pytesseract.image_to_string(
                processed,
                lang=self.lang,
                config='--psm 6 --oem 3'
            )
            
            return text.strip()
            
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return ""
    
    def extract_text_with_roi(self, image, roi_percent=0.6):
        """
        ສະກັດຂໍ້ຄວາມສະເພາະພື້ນທີ່ກາງຂອງຮູບ
        (ຫຼຸດການອ່ານ UI elements)
        
        Args:
            image: ຮູບພາບ (numpy array)
            roi_percent: ເປີເຊັນຂອງພື້ນທີ່ທີ່ຈະໃຊ້ (0-1)
        
        Returns:
            str: ຂໍ້ຄວາມທີ່ອ່ານໄດ້
        """
        h, w = image.shape[:2]
        
        # ເລືອກພື້ນທີ່ກາງ
        top = int(h * (1 - roi_percent) / 2)
        bottom = int(h * (1 + roi_percent) / 2)
        left = int(w * (1 - roi_percent) / 2)
        right = int(w * (1 + roi_percent) / 2)
        
        roi = image[top:bottom, left:right]
        return self.extract_text(roi)
    
    def extract_text_from_file(self, filepath, preprocess=True):
        """
        ສະກັດຂໍ້ຄວາມຈາກໄຟລ໌ຮູບພາບ
        
        Args:
            filepath: ທີ່ຢູ່ຂອງໄຟລ໌ຮູບ
            preprocess: ປັບປຸງຮູບກ່ອນ OCR ຫຼືບໍ່
        
        Returns:
            str: ຂໍ້ຄວາມທີ່ອ່ານໄດ້
        """
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return ""
        
        image = cv2.imread(filepath)
        if image is None:
            print(f"❌ Cannot read image: {filepath}")
            return ""
        
        return self.extract_text(image, preprocess)


def test_ocr():
    """ທົດສອບ OCR"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ OCR")
    print("=" * 60)
    
    # ສ້າງ OCR Reader
    reader = OCRReader(lang="eng+lao")
    
    # ຊອກຫາຮູບພາບຫຼ້າສຸດ
    screenshots_dir = "data/screenshots"
    if not os.path.exists(screenshots_dir):
        print("❌ ບໍ່ມີໂຟນເດີ screenshots")
        return
    
    # ຫາຮູບພາບຫຼ້າສຸດ
    files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
    if not files:
        print("❌ ບໍ່ມີຮູບພາບໃນໂຟນເດີ screenshots")
        print("💡 ຮັນ screen_capture.py ກ່ອນ")
        return
    
    latest = sorted(files)[-1]
    filepath = os.path.join(screenshots_dir, latest)
    
    print(f"📸 ຮູບພາບ: {filepath}")
    
    # ອ່ານຂໍ້ຄວາມ
    print("📝 ກຳລັງອ່ານຂໍ້ຄວາມ...")
    text = reader.extract_text_from_file(filepath)
    
    print("\n" + "=" * 60)
    print("📝 ຂໍ້ຄວາມທີ່ອ່ານໄດ້:")
    print("=" * 60)
    print(text if text else "(ບໍ່ພົບຂໍ້ຄວາມ)")
    print("=" * 60)
    
    # ສະແດງສະຖິຕິ
    if text:
        lines = text.split('\n')
        print(f"\n📊 ຈຳນວນບັນທັດ: {len(lines)}")
        print(f"📊 ຈຳນວນຕົວອັກສອນ: {len(text)}")
    
    print("\n✅ ການທົດສອບສຳເລັດ!")


if __name__ == "__main__":
    test_ocr()