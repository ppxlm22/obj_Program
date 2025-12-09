import sys
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("หน้าต่างเปล่า - PySide6")
window.resize(400, 300)
window.show()

sys.exit(app.exec())