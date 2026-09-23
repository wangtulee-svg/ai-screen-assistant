"""
app_final.py
ໄຟລ໌ຫຼັກສຳລັບ .exe - ລວມ AI Solver V3
"""

import sys
import os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    
sys.path.insert(0, application_path)

from src.overlay import run_overlay
from src.ocr_fast import FastOCR
from src.screen_capture import ScreenCapture
from src.ai_solver_v3 import AISolverV3

class FinalApp:
    def __init__(self):
        self.capturer = ScreenCapture()
        self.ocr = FastOCR(lang="eng")
        self.solver = AISolverV3()
        
        print("AI Screen Assistant ພ້ອມໃຊ້ງານ!")
        
    def scan(self):
        try:
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
            print(f" Error: {e}")
            return None
        
def main():
    """ຟັງຊັນຫຼັກ"""
    
    print("=" * 60)
    print("🤖 AI Screen Assistant - Final")
    print("=" * 60)
    print("ກຳລັງເປີດ...")
    print()
    print("💡 ກົດປຸ່ມ 'ສະແກນ' ໃນ Overlay ເພື່ອສະແກນ")
    print("💡 ກົດປຸ່ມ '✕' ເພື່ອປິດ")
    print("=" * 60)
    
    app = FinalApp()
    run_overlay(app.scan)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 ປິດໂປຣແກຣມ")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("ກົດ Enter ເພື່ອປິດ...")