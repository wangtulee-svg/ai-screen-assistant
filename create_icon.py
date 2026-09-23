"""
create_icon.py
ສ້າງ Icon ສວຍງາມດ້ວຍ Python
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os


def create_icon(size=512, output="new_icon.png"):
    """ສ້າງ Icon ສວຍງາມ"""
    
    # ສ້າງຮູບພື້ນຫຼັງ
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # ============================================================
    # 1. ພື້ນຫຼັງ Gradient (ສີຟ້າເຂັ້ມ → ສີດຳ)
    # ============================================================
    for y in range(size):
        # Gradient ຈາກສີຟ້າເຂັ້ມ (20, 20, 40) → ສີດຳ (5, 5, 15)
        ratio = y / size
        r = int(20 * (1 - ratio) + 5 * ratio)
        g = int(20 * (1 - ratio) + 5 * ratio)
        b = int(40 * (1 - ratio) + 15 * ratio)
        
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # ============================================================
    # 2. ຂອບມົນ (Rounded Rectangle Mask)
    # ============================================================
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    corner_radius = int(size * 0.22)
    mask_draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=255
    )
    
    # ສ້າງຮູບໃໝ່ທີ່ມີຂອບມົນ
    rounded = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    rounded.paste(img, (0, 0), mask)
    img = rounded
    draw = ImageDraw.Draw(img)
    
    # ============================================================
    # 3. ວົງມົນ Neon ສີຂຽວ (Glow Effect)
    # ============================================================
    center = size // 2
    
    # ວົງມົນນອກ (Glow)
    for i in range(8, 0, -1):
        alpha = int(255 * (i / 8) * 0.15)
        radius = int(size * 0.32) + i * 3
        draw.ellipse(
            [(center - radius, center - radius),
             (center + radius, center + radius)],
            outline=(0, 255, 136, alpha),
            width=2
        )
    
    # ວົງມົນຫຼັກ
    radius = int(size * 0.32)
    draw.ellipse(
        [(center - radius, center - radius),
         (center + radius, center + radius)],
        outline=(0, 255, 136, 255),
        width=max(3, size // 100)
    )
    
    # ============================================================
    # 4. ສະໝອງ AI (Brain/AI Symbol)
    # ============================================================
    brain_size = int(size * 0.35)
    
    # ສ້າງຈຸດສຳລັບ Neural Network
    points = []
    layers = [3, 4, 3]
    
    layer_spacing = brain_size // (len(layers) + 1)
    node_radius = max(4, size // 80)
    
    for layer_idx, num_nodes in enumerate(layers):
        x = center - brain_size // 2 + (layer_idx + 1) * layer_spacing
        for node_idx in range(num_nodes):
            y = center - (num_nodes - 1) * layer_spacing // 2 + node_idx * layer_spacing
            points.append((layer_idx, x, y))
    
    # ແຕ້ມເສັ້ນເຊື່ອມ
    for p1 in points:
        for p2 in points:
            if p2[0] == p1[0] + 1:
                draw.line(
                    [(p1[1], p1[2]), (p2[1], p2[2])],
                    fill=(0, 255, 136, 150),
                    width=max(1, size // 200)
                )
    
    # ແຕ້ມຈຸດ
    for layer_idx, x, y in points:
        # ສີຂຽວສຳລັບ layer ກາງ, ສີຟ້າສຳລັບ layer ອື່ນ
        if layer_idx == 1:
            color = (0, 255, 136, 255)
        else:
            color = (100, 200, 255, 255)
        
        # Glow
        for i in range(3, 0, -1):
            glow_radius = node_radius + i * 2
            alpha = int(255 * (i / 3) * 0.3)
            draw.ellipse(
                [(x - glow_radius, y - glow_radius),
                 (x + glow_radius, y + glow_radius)],
                fill=(0, 255, 136, alpha)
            )
        
        # ຈຸດຫຼັກ
        draw.ellipse(
            [(x - node_radius, y - node_radius),
             (x + node_radius, y + node_radius)],
            fill=color
        )
    
    # ============================================================
    # 5. ສັນຍະລັກ "AI" ຢູ່ລຸ່ມ
    # ============================================================
    text = "AI"
    
    try:
        # ລອງໃຊ້ font ທີ່ມີຢູ່
        font_size = int(size * 0.12)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # ຖ້າບໍ່ມີ, ໃຊ້ default
        font = ImageFont.load_default()
    
    # ຫາຕຳແໜ່ງຂອງ text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center - text_width // 2
    text_y = int(size * 0.82)
    
    # Glow ສຳລັບ text
    for offset in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
        draw.text(
            (text_x + offset[0], text_y + offset[1]),
            text,
            fill=(0, 255, 136, 100),
            font=font
        )
    
    # Text ຫຼັກ
    draw.text(
        (text_x, text_y),
        text,
        fill=(0, 255, 136, 255),
        font=font
    )
    
    # ============================================================
    # 6. ບັນທຶກ
    # ============================================================
    img.save(output, "PNG")
    print(f"✅ ສ້າງ Icon ສຳເລັດ: {output}")
    print(f"📁 ຂະໜາດ: {os.path.getsize(output):,} bytes")
    
    return output


def png_to_ico(png_path, ico_path):
    """ແປງ PNG ເປັນ ICO"""
    
    if not os.path.exists(png_path):
        print(f"❌ ບໍ່ພົບ: {png_path}")
        return False
    
    img = Image.open(png_path)
    img = img.convert("RGBA")
    
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format='ICO', sizes=sizes)
    
    print(f"✅ ແປງສຳເລັດ: {ico_path}")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 ສ້າງ Icon ສວຍງາມ")
    print("=" * 60)
    
    # ສ້າງ PNG
    png_file = "new_icon.png"
    create_icon(size=512, output=png_file)
    
    # ແປງເປັນ ICO
    ico_file = "app_icon.ico"
    png_to_ico(png_file, ico_file)
    
    print("=" * 60)
    print("✅ ສຳເລັດ!")
    print("=" * 60)