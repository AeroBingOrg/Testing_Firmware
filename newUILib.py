from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import os

class Window(QWidget):
    
    def __init__(self):
        #Make base window
        super().__init__()
        self.resize(500,450)

        '''layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.input = QLineEdit()
        self.input.setFixedWidth(150)
        layout.addWidget(self.input, alignment= Qt.AlignmentFlag.AlignCenter)
 
        button = QPushButton("X")
        button.clicked.connect(self.get)
        layout.addWidget(button)

        button = QPushButton("Done")
        button.clicked.connect(self.input.clear)
        layout.addWidget(button) '''

    def get(self):
        text = self.input.text()
        print(text)

def inputWindow1(window):
    imported = False
    window.setWindowTitle("Import values")
    layout = QVBoxLayout()
    window.setLayout(layout)
    while imported:
        for i in range(0,4):
            window.input = QLineEdit()
            window.input.setFixedWidth(150)
            layout.addWidget(window.input, alignment= Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Done")
        button.clicked.connect(imported = True)
        layout.addWidget(button)

def inputWindow2(window):
    window.setWindowTitle("Import values")
    layout = QVBoxLayout()
    window.setLayout(layout)
    while True:
        for i in range(0,4):
            window.input = QLineEdit()
            window.input.setFixedWidth(150)
            layout.addWidget(window.input, alignment= Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Done")
        button.clicked.connect(window.get)
        layout.addWidget(button)


def main():
    app = QApplication(sys.argv)
    window = Window()
    inputWindow1(window)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
  main()