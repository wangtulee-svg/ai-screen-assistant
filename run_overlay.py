"""
run_overlay.py
ເປີດ Overlay ພ້ອມກັບ Scanner
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.overlay import run_overlay
from src.ai_solver import AISolver
from src.screen_capture import ScreenCapture
from src.ocr import OCRReader


class ScannerService:
    """ບໍລິການສະແກນ"""
    
    def __init__(self, region=None):
        self.capturer = ScreenCapture()
        self.ocr = OCRReader(lang="eng")
        self.solver = AISolver()
        self.region = region
    
    def scan(self):
        """ສະແກນ ແລະ ຕອບຄຳຖາມ"""
        import cv2
        import numpy as np
        
        # ຈັບພາບ
        if self.region:
            image = self.capturer.capture_region(
                self.region['left'],
                self.region['top'],
                self.region['width'],
                self.region['height']
            )
        else:
            image = self.capturer.capture_full_screen()
        
        # OCR
        text = self.ocr.extract_text(image)
        
        if not text:
            return None
        
        # ວິເຄາະ MCQ
        from src.question_analyzer import QuestionAnalyzer
        analyzer = QuestionAnalyzer()
        result = analyzer.analyze_text(text)
        
        if result['mcq']['is_mcq']:
            mcq = result['mcq']
            
            # ຕອບຄຳຖາມ
            answer = self.solver.solve_mcq(mcq['question'], mcq['options'])
            
            return {
                "question": mcq['question'],
                "answer": answer['answer'],
                "confidence": answer['confidence']
            }
        
        return None


def main():
    """ຟັງຊັນຫຼັກ"""
    
    print("=" * 60)
    print("🤖 AI Screen Assistant - Overlay Mode")
    print("=" * 60)
    
    print("\n📌 ເລືອກການຕັ້ງຄ່າ:")
    print("  1. ສະແກນທັງໜ້າຈໍ")
    print("  2. ສະແກນສະເພາະພື້ນທີ່")
    
    choice = input("\nເລືອກ (1-2): ").strip()
    
    region = None
    
    if choice == "2":
        print("\n📐 ໃສ່ຄ່າພື້ນທີ່")
        try:
            region = {
                "top": int(input("Y (ເທິງ): ")),
                "left": int(input("X (ຊ້າຍ): ")),
                "width": int(input("Width (ກວ້າງ): ")),
                "height": int(input("Height (ສູງ): "))
            }
        except ValueError:
            print("❌ ກະລຸນາໃສ່ຕົວເລກ")
            return
    
    # ສ້າງ Service
    service = ScannerService(region)
    
    print("\n✅ ກຳລັງເປີດ Overlay...")
    print("💡 ກົດປຸ່ມ 'ສະແກນ' ເພື່ອສະແກນ")
    print("💡 ກົດປຸ່ມ 'ອັດຕະໂນມັດ' ເພື່ອສະແກນອັດຕະໂນມັດ")
    print("=" * 60)
    
    # ເລີ່ມ Overlay
    run_overlay(service.scan)


if __name__ == "__main__":
    main()