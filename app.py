from PySide6.QtWidgets import QApplication
from main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.showMaximized()
app.exec()