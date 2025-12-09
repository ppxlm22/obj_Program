import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ultralytics import YOLO 

class FruitDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.model = None
        try:
            self.model = YOLO("success_model_train\\detect_fruit.pt")
        except Exception:
            pass

        self.setWindowTitle("Simple Window")
        self.resize(800, 500)

        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid gray;")
        self.image_label.setText("Area for Image Display")
        self.image_label.setFixedSize(500, 250)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()

        self.btn_browse = QPushButton("Browse Image")
        self.btn_browse.clicked.connect(self.load_image)
        button_layout.addWidget(self.btn_browse)

        self.btn_detect = QPushButton("Detect")
        self.btn_detect.clicked.connect(self.detect_image)
        button_layout.addWidget(self.btn_detect)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def detect_image(self):
        if not self.image_path:
            return

        if self.model is None:
            return

        frame = cv2.imread(self.image_path)
        if frame is None:
            return

        results = self.model.predict(source=frame, conf=0.7, show=False)
        result_frame = results[0].plot()

        cv2.imshow("Detection", result_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FruitDetectionApp()
    window.show()
    sys.exit(app.exec_())