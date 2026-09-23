"""
main.py
AI Screen Assistant - ໂຄດຫຼັກ (ສົມບູນ)
"""

import os
import time
import sys
from datetime import datetime

# ເພີ່ມ path ສຳລັບ import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.screen_capture import ScreenCapture
from src.ocr import OCRReader
from src.question_analyzer import QuestionAnalyzer
from src.ai_solver import AISolver


class AIScreenAssistant:
    """AI Screen Assistant ຫຼັກ"""
    
    def __init__(self):
        """ຕັ້ງຄ່າ"""
        print("=" * 60)
        print("🤖 AI Screen Assistant")
        print("=" * 60)
        
        # ສ້າງຕົວເຮັດວຽກ
        self.capturer = ScreenCapture()
        self.ocr = OCRReader(lang="eng+lao")
        self.analyzer = QuestionAnalyzer()
        self.solver = AISolver()
        
        print("✅ ພ້ອມໃຊ້ງານ!")
        print("=" * 60)
    
    def scan_and_analyze(self, use_roi=True):
        """
        ສະແກນຈໍ ແລະ ວິເຄາະ MCQ
        
        Args:
            use_roi: ໃຊ້ ROI ເພື່ອຫຼຸດສິ່ງລົບກວນ
        """
        print("\n📸 ກຳລັງຈັບພາບຈໍ...")
        
        # 1. ຈັບພາບ
        image = self.capturer.capture_full_screen()
        
        # 2. ບັນທຶກຮູບ (ເຜີຍແຜ່)
        filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.capturer.save_screenshot(image, filename)
        
        # 3. OCR ອ່ານຂໍ້ຄວາມ
        print("📝 ກຳລັງອ່ານຂໍ້ຄວາມ...")
        
        if use_roi:
            # ໃຊ້ ROI ເພື່ອຫຼຸດສິ່ງລົບກວນ
            text = self.ocr.extract_text_with_roi(image, roi_percent=0.6)
        else:
            # ອ່ານທັງຮູບ
            text = self.ocr.extract_text(image)
        
        if not text:
            print("❌ ບໍ່ພົບຂໍ້ຄວາມ")
            return None
        
        print(f"📊 ອ່ານໄດ້ {len(text)} ຕົວອັກສອນ")
        
        # 4. ວິເຄາະຄຳຖາມ
        print("🔍 ກຳລັງວິເຄາະຄຳຖາມ...")
        result = self.analyzer.analyze_text(text)
        
        # ກັ່ນຕອງຕົວເລືອກອີກຄັ້ງ
        if result['mcq']['is_mcq']:
            result['mcq']['options'] = self.analyzer.clean_options(result['mcq']['options'])
        
        return result
    
    def scan_loop(self, interval=2):
        """
        ສະແກນຈໍແບບຕໍ່ເນື່ອງ
        
        Args:
            interval: ໄລຍະຫ່າງລະຫວ່າງການສະແກນ (ວິນາທີ)
        """
        print(f"\n🔄 ເລີ່ມສະແກນອັດຕະໂນມັດ (ທຸກ {interval} ວິນາທີ)")
        print("   ກົດ Ctrl+C ເພື່ອຢຸດ")
        print("-" * 60)
        
        try:
            while True:
                result = self.scan_and_analyze(use_roi=True)
                
                if result and result['mcq']['is_mcq']:
                    print("\n" + "=" * 60)
                    print("📝 ພົບ MCQ!")
                    print("=" * 60)
                    print(f"ຄຳຖາມ: {result['mcq']['question']}")
                    print("\nຕົວເລືອກ:")
                    for i, opt in enumerate(result['mcq']['options']):
                        print(f"  {chr(65+i)}. {opt}")
                    
                    # ໃຊ້ AI Solver
                    print("\n🤖 ກຳລັງຊອກຄຳຕອບ...")
                    answer = self.solver.solve_mcq(
                        result['mcq']['question'],
                        result['mcq']['options']
                    )
                    
                    print(f"\n✅ ຄຳຕອບ: {answer['answer']}")
                    print(f"📊 ຄວາມໝັ້ນໃຈ: {answer['confidence'] * 100}%")
                    print(f"💡 ຄຳອະທິບາຍ: {answer['explanation']}")
                    print("=" * 60)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 ຢຸດການສະແກນ")
    
    def run_once(self):
        """ສະແກນຈໍ 1 ຄັ້ງ"""
        result = self.scan_and_analyze(use_roi=True)
        
        if result:
            print("\n" + "=" * 60)
            print("📊 ສະຫຼຸບການວິເຄາະ")
            print("=" * 60)
            print(f"ຈຳນວນບັນທັດ: {result['stats']['total_lines']}")
            print(f"ເປັນຄຳຖາມ: {result['stats']['has_question']}")
            print(f"ມີຕົວເລືອກ: {result['stats']['has_options']}")
            print(f"ເປັນ MCQ: {result['stats']['is_mcq']}")
            print(f"ຄວາມໝັ້ນໃຈ: {result['stats']['confidence'] * 100}%")
            
            if result['mcq']['is_mcq']:
                print("\n📝 MCQ ທີ່ພົບ:")
                print(f"  ຄຳຖາມ: {result['mcq']['question']}")
                print("  ຕົວເລືອກ:")
                for i, opt in enumerate(result['mcq']['options']):
                    print(f"    {chr(65+i)}. {opt}")
                
                # ໃຊ້ AI Solver
                print("\n🤖 ກຳລັງຊອກຄຳຕອບ...")
                answer = self.solver.solve_mcq(
                    result['mcq']['question'],
                    result['mcq']['options']
                )
                
                print(f"\n✅ ຄຳຕອບ: {answer['answer']}")
                print(f"📊 ຄວາມໝັ້ນໃຈ: {answer['confidence'] * 100}%")
                print(f"💡 ຄຳອະທິບາຍ: {answer['explanation']}")
            else:
                print("\n⚠️ ບໍ່ພົບ MCQ")
            
            print("=" * 60)


def main():
    """ຟັງຊັນຫຼັກ"""
    assistant = AIScreenAssistant()
    
    print("\n📌 ເລືອກໂໝດການໃຊ້ງານ:")
    print("  1. ສະແກນ 1 ຄັ້ງ (ທັງໜ້າຈໍ)")
    print("  2. ສະແກນຕໍ່ເນື່ອງ (ທຸກ 2 ວິນາທີ)")
    print("  3. ສະແກນສະເພາະພື້ນທີ່ (ແນະນຳ)")
    print("  4. ສະແກນຕໍ່ເນື່ອງສະເພາະພື້ນທີ່")
    
    choice = input("\nເລືອກ (1-3): ").strip()
    
    if choice == "1":
        assistant.run_once()
    elif choice == "2":
        assistant.scan_loop(interval=2)
    elif choice == "3":
        assistant.scan_loop(interval=5)
    else:
        print("❌ ເລືອກບໍ່ຖືກຕ້ອງ")


if __name__ == "__main__":
    main()