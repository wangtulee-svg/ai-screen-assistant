"""
app_launcher.py
ເປີດໂປຣແກຣມຫຼັກ - ໃຊ້ສຳລັບແປງເປັນ .exe
"""

import sys
import os

# ຕັ້ງຄ່າ path ສຳລັບ .exe
if getattr(sys, 'frozen', False):
    # ຖ້າຮັນຈາກ .exe
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    # ຖ້າຮັນຈາກ Python
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# ນຳເຂົ້າໂມດູນ
from src.overlay import run_overlay
from src.ocr_improved import ImprovedOCR
from src.screen_capture import ScreenCapture
from src.ai_solver_v2 import AISolverV2


class AppScanner:
    """ບໍລິການສະແກນ"""
    
    def __init__(self):
        self.capturer = ScreenCapture()
        self.ocr = ImprovedOCR(lang="eng")
        self.solver = AISolverV2()
    
    def scan(self):
        """ສະແກນ ແລະ ຕອບຄຳຖາມ"""
        try:
            image = self.capturer.capture_full_screen()
            mcq = self.ocr.extract_structured_mcq(image)
            
            if mcq and mcq['is_mcq']:
                answer = self.solver.solve_mcq(mcq['question'], mcq['options'])
                return {
                    "question": mcq['question'],
                    "answer": answer['answer'],
                    "confidence": answer['confidence']
                }
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None


def main():
    """ເລີ່ມໂປຣແກຣມ"""
    print("=" * 60)
    print("🤖 AI Screen Assistant")
    print("=" * 60)
    print("ກຳລັງເປີດ...")
    
    scanner = AppScanner()
    run_overlay(scanner.scan)


if __name__ == "__main__":
    main()