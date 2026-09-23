"""
convert_icon.py
ແປງ PNG → ICO ດ້ວຍ Python
"""

from PIL import Image
import os

def png_to_ico(png_path, ico_path):
    """ແປງ PNG ເປັນ ICO"""
    
    if not os.path.exists(png_path):
        print(f"❌ ບໍ່ພົບ: {png_path}")
        return False
    
    # ເປີດຮູບ
    img = Image.open(png_path)
    
    # ປ່ຽນເປັນ RGBA
    img = img.convert("RGBA")
    
    # ຂະໜາດທີ່ຕ້ອງການ
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # ບັນທຶກເປັນ ICO
    img.save(ico_path, format='ICO', sizes=sizes)
    
    print(f"✅ ສຳເລັດ: {ico_path}")
    return True


if __name__ == "__main__":
    png_file = "Icon_APP_AI.ico"
    ico_file = "app_icon.ico"
    
    if png_to_ico(png_file, ico_file):
        print(f"📁 ຂະໜາດ: {os.path.getsize(ico_file):,} bytes")
    else:
        print("❌ ລົ້ມເຫຼວ")