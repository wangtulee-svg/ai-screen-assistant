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