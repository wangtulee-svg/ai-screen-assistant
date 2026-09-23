"""
src/region_selector.py
ເລືອກພື້ນທີ່ສະເພາະສຳລັບສະແກນ
"""

import cv2
import numpy as np
import pyautogui
import mss
import os
from datetime import datetime


class RegionSelector:
    """ເລືອກ ແລະ ຈັບພາບສະເພາະພື້ນທີ່"""
    
    def __init__(self):
        self.sct = mss.mss()
        self.selected_region = None
    
    def select_region_manual(self):
        """
        ໃຫ້ຜູ້ໃຊ້ພິມຄ່າ x, y, width, height ເຂົ້າໄປ
        """
        print("\n" + "=" * 60)
        print("📐 ເລືອກພື້ນທີ່ສຳລັບສະແກນ")
        print("=" * 60)
        print("💡 ແນະນຳ: ເປີດ Notepad ທີ່ມີ MCQ ແລ້ວວາງໄວ້ກາງຈໍ")
        print("-" * 60)
        
        try:
            x = int(input("X (ຊ້າຍ): "))
            y = int(input("Y (ເທິງ): "))
            width = int(input("Width (ກວ້າງ): "))
            height = int(input("Height (ສູງ): "))
            
            self.selected_region = {
                "top": y,
                "left": x,
                "width": width,
                "height": height
            }
            
            print(f"\n✅ ບັນທຶກພື້ນທີ່: ({x}, {y}) → {width}x{height}")
            return self.selected_region
            
        except ValueError:
            print("❌ ກະລຸນາໃສ່ຕົວເລກເທົ່ານັ້ນ")
            return None
    
    def capture_region(self, region=None):
        """
        ຈັບພາບສະເພາະພື້ນທີ່
        
        Args:
            region: dict {"top", "left", "width", "height"}
        """
        if region is None:
            region = self.selected_region
        
        if region is None:
            print("❌ ຍັງບໍ່ມີພື້ນທີ່ທີ່ເລືອກ")
            return None
        
        screenshot = self.sct.grab(region)
        return np.array(screenshot)
    
    def capture_fullscreen(self):
        """ຈັບພາບທັງໜ້າຈໍ"""
        monitor = self.sct.monitors[1]
        screenshot = self.sct.grab(monitor)
        return np.array(screenshot)
    
    def get_region_from_file(self, filepath):
        """ອ່ານພື້ນທີ່ຈາກໄຟລ໌ config"""
        import json
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None


def test_region():
    """ທົດສອບການເລືອກພື້ນທີ່"""
    
    selector = RegionSelector()
    
    print("=" * 60)
    print("🧪 ທົດສອບ Region Selector")
    print("=" * 60)
    
    # ເລືອກພື້ນທີ່
    region = selector.select_region_manual()
    
    if region:
        # ຈັບພາບ
        image = selector.capture_region(region)
        
        if image is not None:
            # ບັນທຶກ
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"region_{timestamp}.png"
            os.makedirs("data/regions", exist_ok=True)
            filepath = os.path.join("data/regions", filename)
            
            cv2.imwrite(filepath, cv2.cvtColor(image, cv2.COLOR_BGRA2BGR))
            print(f"✅ ບັນທຶກຮູບ: {filepath}")
            
            # ສະແດງຂະໜາດ
            print(f"📊 ຂະໜາດ: {image.shape}")


if __name__ == "__main__":
    test_region()