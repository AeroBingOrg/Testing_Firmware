from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import os

class Window(QWidget):
    
    def main():

        def submit():
            lower_thrust = lower_thrust_input.text()
            print(lower_thrust)

        app = QApplication(sys.argv)
        window = QWidget()
        window.resize(500,450)
        window.setWindowTitle("Import values")

        layout = QVBoxLayout()
        window.setLayout(layout)

        lower_thrust_label = QLabel("Lower Thrust: ")
        lower_thrust_input = QLineEdit()


        button = QPushButton("X")
        button.clicked.connect(submit)
        layout.addWidget(button)

        window.show()

        sys.exit(app.exec())

    if __name__ == "__main__":
        main()