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

    def inputWindow1(window):
        end = False

        def stop():
            end = True

        window.setWindowTitle("Import values")
        layout = QVBoxLayout()
        window.setLayout(layout)
        while not end:
            for i in range(0,4):
                window.input = QLineEdit()
                window.input.setFixedWidth(150)
                layout.addWidget(window.input, alignment= Qt.AlignmentFlag.AlignCenter)

            button = QPushButton("Done")
            button.clicked.connect(stop())
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
    inputWindow1(window) #doesnt work rn 
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
  main()