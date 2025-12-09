import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QPushButton, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ultralytics import YOLO 
import cv2
from pygame import mixer
import numpy as np

path_img = ""

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Simple Window")
window.resize(800, 500)

layout = QVBoxLayout() 

image_label = QLabel() 
image_label.setAlignment(Qt.AlignCenter) 
image_label.setStyleSheet("border: 2px solid gray;") 

image_label.setText("Area for Image Display")
image_label.setFixedSize(500, 250)

layout.addWidget(image_label, alignment=Qt.AlignCenter)

btn_browse = QPushButton("Browse Image")
layout.addWidget(btn_browse, alignment=Qt.AlignCenter)

def load_image():
    file_name, _ = QFileDialog.getOpenFileName(window, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
    
    if file_name:
        pixmap = QPixmap(file_name)
        scaled_pixmap = pixmap.scaled(image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)

btn_browse.clicked.connect(load_image)

window.setLayout(layout)
window.show()
model = YOLO("success_model_train\\detect_fruit.pt")
image = cv2.imread(path_img)
def detect():
    frame = image
    if frame is None:
        print("Image not found")
        exit(0)
    predict_frame = model.predict(source=frame, conf=0.7, show=False)[0].plot()
    cv2.imshow("Detection", predict_frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        exit(0)
    cv2.destroyAllWindows()

sys.exit(app.exec())

