"""
run_advanced.py
ເປີດ Overlay ກັບ Fast OCR + Multi-Language
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.overlay import run_overlay
from src.ocr_fast import FastOCR
from src.screen_capture import ScreenCapture
from src.ai_solver_v2 import AISolverV2


class AdvancedScannerService:
    """ບໍລິການສະແກນຂັ້ນສູງ"""
    
    def __init__(self, region=None, lang="eng"):
        self.capturer = ScreenCapture()
        self.ocr = FastOCR(lang=lang)
        self.solver = AISolverV2()
        self.region = region
        
        print("✅ Advanced Scanner ພ້ອມ!")
    
    def scan(self):
        """ສະແກນ ແລະ ຕອບ"""
        try:
            if self.region:
                image = self.capturer.capture_region(
                    self.region['left'],
                    self.region['top'],
                    self.region['width'],
                    self.region['height']
                )
            else:
                image = self.capturer.capture_full_screen()
            
            mcq = self.ocr.extract_structured_mcq_fast(image)
            
            if mcq and mcq['is_mcq']:
                answer = self.solver.solve_mcq(mcq['question'], mcq['options'])
                return {
                    "question": mcq['question'],
                    "answer": answer['answer'],
                    "confidence": answer['confidence']
                }
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    """ຟັງຊັນຫຼັກ"""
    
    print("=" * 60)
    print("🤖 AI Screen Assistant - Advanced")
    print("=" * 60)
    
    print("\n📌 ເລືອກພາສາ:")
    print("  1. ອັງກິດ")
    print("  2. ລາວ + ອັງກິດ")
    print("  3. ໄທ + ອັງກິດ")
    
    lang_choice = input("\nເລືອກ (1-3): ").strip()
    
    lang_map = {"1": "eng", "2": "lao+eng", "3": "tha+eng"}
    lang = lang_map.get(lang_choice, "eng")
    
    print(f"\n✅ ພາສາ: {lang}")
    
    service = AdvancedScannerService(lang=lang)
    
    print("\n✅ ກຳລັງເປີດ Overlay...")
    print("=" * 60)
    
    run_overlay(service.scan)


if __name__ == "__main__":
    main()