import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage,QFont
from ultralytics import YOLO 


class FruitDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.model = None
        self.q_img = None
        try:
            self.model = YOLO("success_model_train\\detect_fruit.pt")
        except Exception:
            print("Error loading model.")

        self.setWindowTitle("Ai Fruit Detection")
        self.resize(800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b; 
                color: #ffffff;             
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
            }
            QLabel#TitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #00ff7f; 
                padding: 10px;
            }
            QLabel#ImageArea {
                background-color: #1e1e1e;
                border: 2px dashed #555555; 
                border-radius: 10px;
            }
            QPushButton {
                background-color: #3e3e42;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #505055; 
            }
            QPushButton#BtnDetect {
                background-color: #007acc; 
            }
            QPushButton#BtnDetect:hover {
                background-color: #0098ff;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        self.title_label = QLabel("Fruit Detection System")
        self.title_label.setObjectName("TitleLabel") 
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.image_label = QLabel()
        self.image_label.setObjectName("ImageArea")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Drop Image Here or Browse")
        self.image_label.setSizePolicy(self.image_label.sizePolicy().Expanding, self.image_label.sizePolicy().Expanding)
        self.main_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()

        self.btn_browse = QPushButton("Browse Image")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.load_image)
        button_layout.addWidget(self.btn_browse)

        self.btn_detect = QPushButton("Detect")
        self.btn_detect.setObjectName("BtnDetect")
        self.btn_detect.clicked.connect(self.detect_image)
        button_layout.addWidget(self.btn_detect)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        self.main_layout.addWidget(button_container, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            w = self.image_label.width()
            h = self.image_label.height()
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.image_label.setPixmap(scaled_pixmap)

            self.image_label.setStyleSheet("border: 2px solid #00ff7f; border-radius: 10px;")

    def detect_image(self):
        if not self.image_path:
            return

        if self.model is None:
            return

        frame = cv2.imread(self.image_path)
        if frame is None:
            return

        results = self.model.predict(source=frame, conf=0.7, verbose=False)
        result_frame = results[0].plot()

        height, width, channel = result_frame.shape
        bypt_per_line = 3 * width
        q_img = QImage(result_frame.data, width, height, bypt_per_line, QImage.Format_RGB888).rgbSwapped()

        q_pixmap = QPixmap.fromImage(q_img)

        w = self.image_label.width()
        h = self.image_label.height()
        scaled_pixmap = q_pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

        self.title_label.setText("Detection Complete")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)

    window = FruitDetectionApp()
    window.show()
    sys.exit(app.exec_())