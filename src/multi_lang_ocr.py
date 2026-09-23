"""
src/multi_lang_ocr.py
OCR ຮອງຮັບຫຼາຍພາສາ
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image


class MultiLangOCR:
    """OCR ຮອງຮັບຫຼາຍພາສາ"""
    
    # ພາສາທີ່ຮອງຮັບ
    LANGUAGES = {
        "english": "eng",
        "lao": "lao",
        "thai": "tha",
        "chinese": "chi_sim",
        "japanese": "jpn",
        "korean": "kor",
        "french": "fra",
        "spanish": "spa",
    }
    
    def __init__(self, languages=None):
        """
        ຕັ້ງຄ່າ
        
        Args:
            languages: ລາຍຊື່ພາສາ (default: ["english"])
        """
        if languages is None:
            languages = ["english"]
        
        self.lang_codes = [
            self.LANGUAGES.get(lang, lang)
            for lang in languages
        ]
        self.lang_string = "+".join(self.lang_codes)
        
        print(f"✅ ພາສາທີ່ໃຊ້: {self.lang_string}")
    
    def extract_text(self, image):
        """ອ່ານຂໍ້ຄວາມ"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # ແປງເປັນ Grayscale
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # ປັບຂະໜາດ
        h, w = gray.shape
        scale = 2.0
        resized = cv2.resize(gray, (int(w * scale), int(h * scale)))
        
        # ເພີ່ມຄວາມຄົມຊັດ
        _, thresh = cv2.threshold(resized, 0, 255,
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OCR
        try:
            text = pytesseract.image_to_string(
                thresh,
                lang=self.lang_string,
                config='--psm 6 --oem 3'
            )
            return text.strip()
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""


def test_multi_lang():
    """ທົດສອບ Multi-Language OCR"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Multi-Language OCR")
    print("=" * 60)
    
    # ທົດສອບພາສາອັງກິດ
    print("\n📌 ອັງກິດ:")
    ocr_en = MultiLangOCR(["english"])
    
    # ທົດສອບພາສາລາວ + ອັງກິດ
    print("\n📌 ລາວ + ອັງກິດ:")
    ocr_lao = MultiLangOCR(["lao", "english"])
    
    print("\n✅ ພ້ອມໃຊ້ງານ!")


if __name__ == "__main__":
    test_multi_lang()