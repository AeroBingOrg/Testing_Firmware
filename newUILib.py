from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import os

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.resize(300,250)
        self.setWindowTitle("Enter values")

        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.input = QLineEdit()
        self.input.setFixedWidth(150)
        layout.addWidget(self.input, alignment= Qt.AlignmentFlag.AlignCenter)
 
        button = QPushButton("X")
        button.clicked.connect(self.get)
        layout.addWidget(button)

        button = QPushButton("Done")
        button.clicked.connect(self.input.clear)
        layout.addWidget(button)

    def get(self):
        text = self.input.text()
        print(text)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
  main()