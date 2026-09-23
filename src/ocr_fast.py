"""
src/ocr_fast.py
OCR ທີ່ປັບປຸງໃຫ້ໄວຂຶ້ນ - ຮອງຮັບຫຼາຍ MCQ
"""

import cv2
"""
src/overlay.py
Overlay ໂປ່ງໃສສຳລັບສະແດງຄຳຕອບ - ຮອງຮັບຫຼາຍ MCQ
"""

import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QWidget, QPushButton, QHBoxLayout, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor


class AnswerOverlay(QMainWindow):
    """Overlay ສະແດງຄຳຕອບ"""
    
    # Signal ສຳລັບອັບເດດຄຳຕອບ
    answers_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
        # ຕັ້ງຄ່າ Window
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # ຕຳແໜ່ງ ແລະ ຂະໜາດ
        self.setGeometry(50, 50, 500, 400)
        
        # ສ້າງ Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # ຕັ້ງຄ່າສີ
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 220);
                border-radius: 15px;
                border: 2px solid #00ff88;
            }
            QLabel {
                color: #00ff88;
                font-family: 'Arial';
                font-size: 14px;
                padding: 5px;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 20);
                color: #ffffff;
                border: 1px solid rgba(0, 255, 136, 0.3);
                border-radius: 8px;
                font-family: 'Arial';
                font-size: 13px;
                padding: 8px;
            }
            QPushButton {
                background-color: rgba(0, 255, 136, 0.2);
                color: #00ff88;
                border: 1px solid #00ff88;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 136, 0.4);
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self.central_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("🤖 AI Screen Assistant")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff88;")
        header.addWidget(title)
        
        header.addStretch()
        
        # ປຸ່ມປິດ
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.3);
                color: #ff4444;
                border: 1px solid #ff4444;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.6);
            }
        """)
        close_btn.clicked.connect(self.hide)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # ສະຖານະ
        self.status_label = QLabel("🔍 ກຳລັງລໍຖ້າ...")
        self.status_label.setStyleSheet("font-size: 12px; color: #ffff88;")
        layout.addWidget(self.status_label)
        
        # ຄຳຖາມ
        self.question_label = QLabel("📝 ຄຳຖາມ: -")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 13px; color: #ffffff;")
        layout.addWidget(self.question_label)
        
        # ຄຳຕອບ (ຮອງຮັບຫຼາຍຄຳຕອບ)
        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)
        self.answer_text.setPlaceholderText("ຄຳຕອບຈະສະແດງຢູ່ນີ້...")
        layout.addWidget(self.answer_text)
        
        # ປຸ່ມຄວບຄຸມ
        btn_layout = QHBoxLayout()
        
        self.scan_btn = QPushButton("🔍 ສະແກນ")
        self.scan_btn.clicked.connect(self.on_scan_clicked)
        btn_layout.addWidget(self.scan_btn)
        
        self.auto_btn = QPushButton("🔄 ອັດຕະໂນມັດ")
        self.auto_btn.setCheckable(True)
        self.auto_btn.clicked.connect(self.on_auto_toggled)
        btn_layout.addWidget(self.auto_btn)
        
        self.clear_btn = QPushButton("🗑️ ລ້າງ")
        self.clear_btn.clicked.connect(self.clear)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # ເຊື່ອມຕໍ່ Signal
        self.answers_updated.connect(self.update_answers)
        
        # ຕົວປ່ຽນ
        self.scanner_callback = None
        self.auto_timer = None
        self.is_auto = False
        self.old_pos = None
        
        # ສະແດງ
        self.show()
    
    def set_scanner_callback(self, callback):
        """ຕັ້ງຄ່າ Callback ສຳລັບການສະແກນ"""
        self.scanner_callback = callback
    
    def on_scan_clicked(self):
        """ເມື່ອກົດປຸ່ມສະແກນ"""
        if self.scanner_callback:
            self.status_label.setText("🔍 ກຳລັງສະແກນ...")
            
            # ຮັນໃນ Thread ແຍກ
            thread = threading.Thread(target=self._do_scan)
            thread.daemon = True
            thread.start()
    
    def _do_scan(self):
        """ສະແກນໃນ Thread"""
        try:
            results = self.scanner_callback()
            self.answers_updated.emit(results if results else [])
        except Exception as e:
            print(f"Error: {e}")
            self.answers_updated.emit([])
    
    def update_answers(self, results):
        """ອັບເດດ UI ດ້ວຍທຸກຄຳຕອບ"""
        self.answer_text.clear()
        
        if not results:
            self.answer_text.setText("⚠️ ບໍ່ພົບ MCQ")
            self.status_label.setText("❌ ບໍ່ພົບ MCQ")
            self.question_label.setText("📝 ຄຳຖາມ: -")
            return
        
        # ສ້າງ output
        output = []
        for i, result in enumerate(results, 1):
            output.append(f"━━━━━━━━━━━━━━━━━━━━")
            output.append(f"📝 ຄຳຖາມທີ {i}: {result['question']}")
            output.append(f"✅ ຄຳຕອບ: {result['answer']}")
            output.append(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence']*100:.0f}%")
            output.append("")
        
        self.answer_text.setText("\n".join(output))
        self.status_label.setText(f"✅ ພົບ {len(results)} ຄຳຖາມ")
        self.question_label.setText(f"📝 ພົບ {len(results)} MCQ")
    
    def on_auto_toggled(self):
        """ເມື່ອເປີດ/ປິດ ອັດຕະໂນມັດ"""
        self.is_auto = self.auto_btn.isChecked()
        
        if self.is_auto:
            self.auto_btn.setText("⏸️ ຢຸດ")
            self.start_auto_scan()
        else:
            self.auto_btn.setText("🔄 ອັດຕະໂນມັດ")
            self.stop_auto_scan()
    
    def start_auto_scan(self):
        """ເລີ່ມສະແກນອັດຕະໂນມັດ"""
        if self.auto_timer is None:
            self.auto_timer = QTimer()
            self.auto_timer.timeout.connect(self.on_scan_clicked)
        
        self.auto_timer.start(3000)
        self.status_label.setText("🔄 ກຳລັງສະແກນອັດຕະໂນມັດ...")
    
    def stop_auto_scan(self):
        """ຢຸດສະແກນອັດຕະໂນມັດ"""
        if self.auto_timer:
            self.auto_timer.stop()
        self.status_label.setText("⏸️ ຢຸດສະແກນ")
    
    def clear(self):
        """ລ້າງຂໍ້ຄວາມ"""
        self.question_label.setText("📝 ຄຳຖາມ: -")
        self.answer_text.clear()
        self.status_label.setText("🔍 ກຳລັງລໍຖ້າ...")
    
    def mousePressEvent(self, event):
        """ເມື່ອກົດ Mouse ເພື່ອຍ້າຍ"""
        self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """ເມື່ອລາກ Mouse"""
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()


def run_overlay(scanner_callback=None):
    """ເລີ່ມ Overlay"""
    app = QApplication(sys.argv)
    overlay = AnswerOverlay()
    
    if scanner_callback:
        overlay.set_scanner_callback(scanner_callback)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    def test_callback():
        return [
            {"question": "What is the capital of Laos?", "answer": "C. Vientiane", "confidence": 0.95},
            {"question": "What is 5 + 3?", "answer": "C. 8", "confidence": 0.95},
            {"question": "Which planet is the Red Planet?", "answer": "B. Mars", "confidence": 0.90},
        ]
    
    run_overlay(test_callback)
import numpy as np
import pytesseract
from PIL import Image
import os
import time
import re
from concurrent.futures import ThreadPoolExecutor
import threading


class FastOCR:
    """OCR ທີ່ໄວຂຶ້ນ"""
    
    def __init__(self, lang="eng"):
        self.lang = lang
        self.cache = {}
        self.cache_lock = threading.Lock()
        
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract Version: {version}")
        except Exception as e:
            print(f"⚠️ Tesseract Error: {e}")
    
    def preprocess_fast(self, image):
        """ປັບປຸງຮູບແບບໄວ"""
        # ແປງເປັນ Grayscale
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # ປັບຂະໜາດໃຫຍ່ຂຶ້ນ
        h, w = gray.shape
        scale = 2.0
        resized = cv2.resize(gray, (int(w * scale), int(h * scale)),
                             interpolation=cv2.INTER_LINEAR)
        
        # ເພີ່ມຄວາມຄົມຊັດແບບໄວ
        _, thresh = cv2.threshold(resized, 0, 255,
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text_fast(self, image, psm=6):
        """ອ່ານຂໍ້ຄວາມແບບໄວ"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        processed = self.preprocess_fast(image)
        
        # ຕັ້ງຄ່າ OCR ໃຫ້ໄວ
        config = f'--psm {psm} --oem 1'  # OEM 1 = LSTM only (ໄວກວ່າ)
        
        try:
            text = pytesseract.image_to_string(
                processed,
                lang=self.lang,
                config=config
            )
            return text.strip()
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return ""
    
    def extract_all_mcqs(self, image):
        """
        ສະກັດທຸກ MCQ ຈາກຮູບ
        
        Returns:
            List[Dict]: ລາຍຊື່ຂອງ MCQ
        """
        # ອ່ານຂໍ້ຄວາມທັງໝົດ
        text = self.extract_text_fast(image)
        
        if not text:
            return []
        
        # ແຍກບັນທັດ
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # ກັ່ນຕອງບັນທັດທີ່ບໍ່ຕ້ອງການ
        cleaned_lines = []
        for line in lines:
            # ຂ້າມບັນທັດທີ່ສັ້ນເກີນ
            if len(line) < 2:
                continue
            
            # ຂ້າມບັນທັດທີ່ມີຕົວອັກສອນພິເສດຫຼາຍ
            special = sum(1 for c in line if not c.isalnum() and c not in ' .,!?-()?:')
            if special > len(line) * 0.5:
                continue
            
            cleaned_lines.append(line)
        
        # ຊອກຫາທຸກ MCQ
        mcqs = []
        current_question = None
        current_options = []
        
        for line in cleaned_lines:
            # ກວດວ່າເປັນຄຳຖາມໃໝ່ບໍ່
            is_new_question = False
            
            # ຖ້າມີ ? ແລະ ບໍ່ແມ່ນຕົວເລືອກ
            if '?' in line and not re.match(r'^[A-Da-d][\.\)]', line):
                is_new_question = True
            
            # ຖ້າຂຶ້ນຕົ້ນດ້ວຍ What/Which/How/Why ແລະ ບໍ່ມີຕົວເລືອກ
            if re.match(r'^(what|which|how|why|who|where|when)', line, re.I):
                if not re.match(r'^[A-Da-d][\.\)]', line):
                    is_new_question = True
            
            if is_new_question:
                # ບັນທຶກ MCQ ເກົ່າ
                if current_question and len(current_options) >= 2:
                    mcqs.append({
                        "question": current_question,
                        "options": current_options.copy(),
                        "is_mcq": True
                    })
                
                # ເລີ່ມໃໝ່
                current_question = line
                current_options = []
                continue
            
            # ກວດວ່າເປັນຕົວເລືອກບໍ່
            match = re.match(r'^([A-Da-d])[\.\)]\s*(.+)$', line)
            if match:
                opt_text = match.group(2).strip()
                # ກັ່ນຕອງ
                if 1 <= len(opt_text) <= 100:
                    current_options.append(opt_text)
        
        # ບັນທຶກ MCQ ສຸດທ້າຍ
        if current_question and len(current_options) >= 2:
            mcqs.append({
                "question": current_question,
                "options": current_options.copy(),
                "is_mcq": True
            })
        
        return mcqs


def test_fast_ocr():
    """ທົດສອບ Fast OCR"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Fast OCR")
    print("=" * 60)
    
    ocr = FastOCR(lang="eng")
    
    # ຊອກຫາຮູບ
    screenshots_dir = "data/screenshots"
    if not os.path.exists(screenshots_dir):
        print("❌ ບໍ່ມີໂຟນເດີ")
        return
    
    files = sorted([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
    if not files:
        print("❌ ບໍ່ມີຮູບ")
        return
    
    latest = files[-1]
    filepath = os.path.join(screenshots_dir, latest)
    
    image = cv2.imread(filepath)
    
    # ທົດສອບຄວາມໄວ
    start = time.time()
    text = ocr.extract_text_fast(image)
    elapsed = time.time() - start
    
    print(f"\n⚡ ເວລາ: {elapsed:.2f} ວິນາທີ")
    print(f"📊 ອ່ານໄດ້: {len(text)} ຕົວອັກສອນ")
    
    print("\n📝 ຂໍ້ຄວາມ:")
    print(text[:500])


if __name__ == "__main__":
    test_fast_ocr()