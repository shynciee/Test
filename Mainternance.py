import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QFrame, QMessageBox,QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomAlert(QDialog):
    def __init__(self, message="Nhập gì i"):
        super().__init__()
        self.setWindowTitle("Ê")
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: white; border-radius: 12px;")

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: #e67e22;")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)

        ok_btn = QPushButton("OK ")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 6px 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class MaintenanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bảo trì 😩")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #f7f7f7;")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(10)

        title = QLabel("🛠️ Hùng đang fix lỗi...")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18 , QFont.Bold))
        title.setStyleSheet("color: #e67e22;")

        desc = QLabel("Hùng đang sửa lỗi lại chút xíu...\nNếu cần gấp thì cứ inbox e Hùng để mở riêng cho nhé 💬")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #444; font-size: 15px;")

        contact = QLabel()
        contact.setTextFormat(Qt.RichText)
        contact.setTextInteractionFlags(Qt.TextBrowserInteraction)
        contact.setOpenExternalLinks(True)
        contact.setAlignment(Qt.AlignCenter)
        contact.setStyleSheet("color: #2c3e50; font-weight: bold;font-size: 15px;")
        contact.setText(
            """
            🌐 <a href='https://facebook.com/shynciee'>Facebook</a> |
            <a href='https://zalo.me/0869983819'>Zalo</a><br>
            📧 <a href='shynciee@gmail.com'>shynciee@gmail.com</a>
            """
        )

        comment_label = QLabel("✍️ Gửi feedback (Ẩn danh):")
        comment_label.setStyleSheet("color: #333; font-weight: bold;font-size: 15px;")
        self.comment_box = QTextEdit()
        self.comment_box.setPlaceholderText("Viết gì đó cho Hùng...")
        self.comment_box.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 5px;")
        self.comment_box.setFixedHeight(60)

        send_btn = QPushButton("Gửi cho Hùng")
        send_btn.clicked.connect(self.send_comment)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)

        frame_layout.addWidget(title)
        frame_layout.addWidget(desc)
        frame_layout.addWidget(contact)
        frame_layout.addWidget(comment_label)
        frame_layout.addWidget(self.comment_box)
        frame_layout.addWidget(send_btn, alignment=Qt.AlignCenter)
        frame_layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        self.setLayout(layout)

    def send_comment(self):
        comment = self.comment_box.toPlainText().strip()
        if not comment:
            alert = CustomAlert("Chưa nhập gì hết mà nhấn gửi😡")
            alert.exec_()
            return

        try:
            response = requests.post(
                "https://backend-api-znlr.onrender.com/feedback",  
                json={"comment": comment},
                timeout=15
            )
            if response.status_code == 200:
                alert = CustomAlert("Ok . Hùng đọc liền đó 👌")
                alert.exec_()
                self.comment_box.clear()
            else:
                QMessageBox.warning(self, "Lỗi", f"Không gửi được: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi mạng", f"Không thể kết nối:\n{e}")

if __name__ == "__main__":
    app = QApplication([])
    window = MaintenanceWindow()
    window.show()
    app.exec_()
