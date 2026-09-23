"""
run_final_v3.py
ເປີດ Overlay ກັບ AI Solver V4 + Knowledge Base ຂະຫຍາຍ
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.overlay import run_overlay
from src.ocr_fast import FastOCR
from src.screen_capture import ScreenCapture
from src.ai_solver_v4 import AISolverV4


class FinalScannerService:
    """ບໍລິການສະແກນສຸດທ້າຍ - ຮອງຮັບຫຼາຍ MCQ"""
    
    def __init__(self, region=None, lang="eng"):
        self.capturer = ScreenCapture()
        self.ocr = FastOCR(lang=lang)
        self.solver = AISolverV4()
        self.region = region
        
        print("✅ Final Scanner Service ພ້ອມໃຊ້ງານ!")
    
    def scan(self):
        """ສະແກນ ແລະ ຕອບທຸກຄຳຖາມ"""
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
            
            # ດຶງທຸກ MCQ
            mcqs = self.ocr.extract_all_mcqs(image)
            
            if not mcqs:
                return []
            
            # ຕອບທຸກຄຳຖາມ
            results = []
            for mcq in mcqs:
                answer = self.solver.solve_mcq(mcq['question'], mcq['options'])
                results.append({
                    "question": mcq['question'],
                    "answer": answer['answer'],
                    "confidence": answer['confidence']
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []


def main():
    """ຟັງຊັນຫຼັກ"""
    
    print("=" * 60)
    print("🤖 AI Screen Assistant - Final V3 (Knowledge Base)")
    print("=" * 60)
    
    print("\n📌 ເລືອກການຕັ້ງຄ່າ:")
    print("  1. ສະແກນທັງໜ້າຈໍ")
    print("  2. ສະແກນສະເພາະພື້ນທີ່")
    
    choice = input("\nເລືອກ (1-2): ").strip()
    
    region = None
    
    if choice == "2":
        print("\n📐 ໃສ່ຄ່າພື້ນທີ່")
        print("💡 ແນະນຳ: X=100, Y=100, Width=800, Height=600")
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
    
    service = FinalScannerService(region)
    
    print("\n✅ ກຳລັງເປີດ Overlay...")
    print("💡 ກົດປຸ່ມ 'ສະແກນ' ເພື່ອສະແກນ")
    print("💡 ກົດປຸ່ມ '✕' ໃນ Overlay ເພື່ອປິດ")
    print("=" * 60)
    
    try:
        run_overlay(service.scan)
    except KeyboardInterrupt:
        print("\n\n👋 ປິດໂປຣແກຣມ")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()