"""
app_v3.py
ໄຟລ໌ຫຼັກສຳລັບ .exe ໃໝ່ - ລວມ AI Solver V3 ແລະ Multi-MCQ
"""

import sys
import os

# ຕັ້ງຄ່າ path ສຳລັບ .exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# ນຳເຂົ້າໂມດູນ
from src.overlay import run_overlay
from src.ocr_fast import FastOCR
from src.screen_capture import ScreenCapture
from src.ai_solver_v3 import AISolverV3


class FinalAppV3:
    """ແອັບພລິເຄຊັນສຸດທ້າຍ V3"""
    
    def __init__(self):
        self.capturer = ScreenCapture()
        self.ocr = FastOCR(lang="eng")
        self.solver = AISolverV3()
        
        print("✅ AI Screen Assistant V3 ພ້ອມໃຊ້ງານ!")
    
    def scan(self):
        """ສະແກນ ແລະ ຕອບທຸກຄຳຖາມ"""
        try:
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
    print("🤖 AI Screen Assistant V3")
    print("=" * 60)
    print("ກຳລັງເປີດ...")
    print()
    print("💡 ກົດປຸ່ມ 'ສະແກນ' ໃນ Overlay ເພື່ອສະແກນ")
    print("💡 ກົດປຸ່ມ '✕' ເພື່ອປິດ")
    print("=" * 60)
    
    app = FinalAppV3()
    
    try:
        run_overlay(app.scan)
    except KeyboardInterrupt:
        print("\n👋 ປິດໂປຣແກຣມ")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("ກົດ Enter ເພື່ອປິດ...")


if __name__ == "__main__":
    main()