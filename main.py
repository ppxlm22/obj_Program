import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Simple Window")
window.resize(800, 500)
window.show()

sys.exit(app.exec_())