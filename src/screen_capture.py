"""
src/screen_capture.py
ຈັບພາບຈໍສະແດງຜົນ ສຳລັບ AI Screen Assistant
"""

import mss
import mss.tools
from PIL import Image
import numpy as np
import os
from datetime import datetime


class ScreenCapture:
    """ຈັບພາບຈໍສະແດງຜົນ"""
    
    def __init__(self):
        """ຕັ້ງຄ່າ Screen Capture"""
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # ຈໍຫຼັກ
        
    def capture_full_screen(self):
        """
        ຈັບພາບທັງໜ້າຈໍ
        
        Returns:
            np.ndarray: ຮູບພາບແບບ numpy array
        """
        screenshot = self.sct.grab(self.monitor)
        return np.array(screenshot)
    
    def capture_region(self, x, y, width, height):
        """
        ຈັບພາບສະເພາະພື້ນທີ່
        
        Args:
            x, y: ຕຳແໜ່ງເລີ່ມຕົ້ນ
            width, height: ຂະໜາດ
        
        Returns:
            np.ndarray: ຮູບພາບແບບ numpy array
        """
        monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }
        screenshot = self.sct.grab(monitor)
        return np.array(screenshot)
    
    def save_screenshot(self, image=None, filename=None):
        """
        ບັນທຶກຮູບພາບ
        
        Args:
            image: ຮູບພາບ (ຖ້າບໍ່ມີ, ຈັບພາບໃໝ່)
            filename: ຊື່ໄຟລ໌ (ຖ້າບໍ່ມີ, ສ້າງອັດຕະໂນມັດ)
        
        Returns:
            str: ຊື່ໄຟລ໌ທີ່ບັນທຶກ
        """
        if image is None:
            image = self.capture_full_screen()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # ສ້າງໂຟນເດີ screenshots ຖ້າບໍ່ມີ
        os.makedirs("data/screenshots", exist_ok=True)
        
        filepath = os.path.join("data/screenshots", filename)
        
        # ແປງເປັນ PIL Image ແລ້ວບັນທຶກ
        Image.fromarray(image).save(filepath)
        
        print(f"✅ ບັນທຶກຮູບພາບ: {filepath}")
        return filepath


def test_capture():
    """ທົດສອບການຈັບພາບ"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Screen Capture")
    print("=" * 60)
    
    # ສ້າງຕົວຈັບພາບ
    capturer = ScreenCapture()
    
    # ຈັບພາບທັງໜ້າຈໍ
    print("📸 ຈັບພາບຈໍ...")
    image = capturer.capture_full_screen()
    
    print(f"📊 ຂະໜາດຮູບ: {image.shape}")
    print(f"📊 ປະເພດຂໍ້ມູນ: {image.dtype}")
    
    # ບັນທຶກຮູບພາບ
    filepath = capturer.save_screenshot(image)
    
    print("=" * 60)
    print("✅ ການທົດສອບສຳເລັດ!")
    print("=" * 60)
    
    return image


if __name__ == "__main__":
    test_capture()