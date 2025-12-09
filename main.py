import sys
# from PySide6.QtWidgets import QApplication, QWidget
from ultralytics import YOLO 
import cv2
from pygame import mixer
import numpy as np



path_img = ""

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("หน้าต่างเปล่า - PySide6")
window.resize(400, 300)
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

if __name__ == "__main__":
    detect()