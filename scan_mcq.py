"""
scan_mcq.py
ສະແກນ ແລະ ຕອບ MCQ ອັດຕະໂນມັດ
"""

import mss
import cv2
import numpy as np
import pytesseract
import time
import os
from datetime import datetime
from src.ai_solver import AISolver

class MCQScanner:
    """ສະແກນ MCQ ຈາກຈໍ ແລະ ຕອບຄຳຖາມ"""
    
    def __init__(self, region=None):
        """
        ຕັ້ງຄ່າ Scanner
        
        Args:
            region: dict {"top": y, "left": x, "width": w, "height": h}
        """
        self.region = region
        self.solver = AISolver()
        self.sct = mss.mss()
        
        # ຖ້າບໍ່ມີ region, ໃຊ້ທັງໜ້າຈໍ
        if region is None:
            self.region = self.sct.monitors[1]
    
    def capture(self):
        """ຈັບພາບ"""
        screenshot = self.sct.grab(self.region)
        return np.array(screenshot)
    
    def extract_text(self, image):
        """ອ່ານຂໍ້ຄວາມຈາກຮູບ"""
        # ແປງເປັນ Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        
        # ປັບຂະໜາດ
        h, w = gray.shape
        scale = 2.0
        resized = cv2.resize(gray, (int(w * scale), int(h * scale)))
        
        # ເພີ່ມຄວາມຄົມຊັດ
        _, thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OCR
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6 --oem 3')
        return text.strip()
    
    def parse_mcq(self, text):
        """
        ວິເຄາະຂໍ້ຄວາມ ແລະ ສະກັດ MCQ
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return None
        
        # ຊອກຫາຄຳຖາມທຳອິດ
        question = None
        options = []
        in_mcq = False
        
        for line in lines:
            # ຊອກຄຳຖາມ
            if '?' in line and not in_mcq:
                question = line
                in_mcq = True
                continue
            
            # ຊອກຕົວເລືອກ
            if in_mcq:
                line_upper = line.upper()
                if line_upper.startswith(('A.', 'B.', 'C.', 'D.')) or line_upper.startswith(('A)', 'B)', 'C)', 'D)')):
                    opt_text = line[2:].strip()
                    options.append(opt_text)
                elif line_upper.startswith(('E.', 'F.')):  # ຖ້າມີຫຼາຍກວ່າ 4 ຂໍ້
                    opt_text = line[2:].strip()
                    options.append(opt_text)
                else:
                    # ຖ້າເຈີບັນທັດທີ່ບໍ່ແມ່ນຕົວເລືອກ, ຢຸດ
                    if len(options) >= 2:
                        break
        
        if question and len(options) >= 2:
            return {
                "question": question,
                "options": options[:6]  # ຈຳກັດສູງສຸດ 6 ຂໍ້
            }
        
        return None
    
    def scan_once(self):
        """ສະແກນ 1 ຄັ້ງ ແລະ ຕອບຄຳຖາມ"""
        print("\n📸 ກຳລັງຈັບພາບ...")
        image = self.capture()
        
        print("📝 ກຳລັງອ່ານຂໍ້ຄວາມ...")
        text = self.extract_text(image)
        
        if not text:
            print("❌ ບໍ່ພົບຂໍ້ຄວາມ")
            return
        
        print(f"📊 ອ່ານໄດ້ {len(text)} ຕົວອັກສອນ")
        
        mcq = self.parse_mcq(text)
        
        if mcq:
            print("\n" + "=" * 60)
            print("✅ ພົບ MCQ!")
            print("=" * 60)
            print(f"📝 ຄຳຖາມ: {mcq['question']}")
            print("📋 ຕົວເລືອກ:")
            for i, opt in enumerate(mcq['options']):
                print(f"   {chr(65+i)}. {opt}")
            
            result = self.solver.solve_mcq(mcq['question'], mcq['options'])
            
            print("\n" + "=" * 60)
            print("🤖 ຄຳຕອບ:")
            print("=" * 60)
            print(f"✅ {result['answer']}")
            print(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence'] * 100}%")
            print(f"💡 {result['explanation']}")
            print("=" * 60)
        else:
            print("\n⚠️ ບໍ່ພົບ MCQ")
    
    def scan_loop(self, interval=3):
        """ສະແກນຕໍ່ເນື່ອງ"""
        print(f"\n🔄 ເລີ່ມສະແກນອັດຕະໂນມັດ (ທຸກ {interval} ວິນາທີ)")
        print("   ກົດ Ctrl+C ເພື່ອຢຸດ")
        print("-" * 60)
        
        try:
            while True:
                self.scan_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n🛑 ຢຸດການສະແກນ")


def main():
    """ຟັງຊັນຫຼັກ"""
    
    print("=" * 60)
    print("🤖 AI Screen MCQ Scanner")
    print("=" * 60)
    
    print("\n📌 ເລືອກວິທີສະແກນ:")
    print("  1. ສະແກນທັງໜ້າຈໍ (ອາດມີສິ່ງລົບກວນ)")
    print("  2. ສະແກນສະເພາະພື້ນທີ່ (ແນະນຳ)")
    print("  3. ອອກ")
    
    choice = input("\nເລືອກ (1-3): ").strip()
    
    if choice == "3":
        print("👋 ພົບກັນໃໝ່!")
        return
    
    if choice == "1":
        scanner = MCQScanner()
        scanner.scan_once()
        
        # ຖາມວ່າຢາກສະແກນອີກບໍ່
        again = input("\nຢາກສະແກນອີກບໍ່? (y/n): ").strip().lower()
        if again == 'y':
            scanner.scan_loop(interval=3)
    
    elif choice == "2":
        print("\n📐 ໃສ່ຄ່າພື້ນທີ່")
        print("💡 ເປີດ Notepad ທີ່ມີ MCQ ໄວ້ກາງຈໍ")
        print("-" * 60)
        
        try:
            x = int(input("X (ຊ້າຍ, ປົກກະຕິ 50-100): "))
            y = int(input("Y (ເທິງ, ປົກກະຕິ 50-100): "))
            w = int(input("Width (ກວ້າງ, ປົກກະຕິ 800-1000): "))
            h = int(input("Height (ສູງ, ປົກກະຕິ 500-700): "))
            
            region = {"top": y, "left": x, "width": w, "height": h}
            scanner = MCQScanner(region)
            
            scanner.scan_once()
            
            # ຖາມວ່າຢາກສະແກນອີກບໍ່
            again = input("\nຢາກສະແກນອີກບໍ່? (y/n): ").strip().lower()
            if again == 'y':
                scanner.scan_loop(interval=3)
                
        except ValueError:
            print("❌ ກະລຸນາໃສ່ຕົວເລກ")
    
    else:
        print("❌ ເລືອກບໍ່ຖືກຕ້ອງ")


if __name__ == "__main__":
    main()