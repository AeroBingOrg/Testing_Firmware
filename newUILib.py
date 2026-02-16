from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QMessageBox
import sys
import os

class Window(QWidget): #Code still is broken, but recreated tkinter ui with PyQt6
    
    def main():

        def submit(): #this runs when you submit your values
            values = {
            'lowerthrust': lower_thrust_input.text(),
            'upperthrust': upper_thrust_input.text(),
            'maxthrust_precent': maxthrust_precent_input.text(),
            'spacing': spacing_input.text()
            }
            print("Lower thrust: " + values['lowerthrust'])
            print("Upper thrust: " + values['upperthrust'])
            print("Max thrust %: " + values['maxthrust_precent'])
            print("Spacing: " + values['spacing'])

            try:
                math = Load_cell_math(values['lowerthrust'], values["upperthrust"], values["maxthrust_precent"], values["spacing"])

                filtered_pressure_above_20N, filtered_thrust_above_20N, filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N = math.calculations()

                testing_UI.plots(filtered_pressure_above_20N, filtered_thrust_above_20N, 
                       filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N)
            except:
                QMessageBox.information(window, "Error", "Failed Calculations & Graphing.")

        app = QApplication(sys.argv)
        
        #Create window
        window = QWidget()
        window.resize(300,200)
        window.setWindowTitle("Import values")

        layout = QFormLayout()

        #Create inputs
        lower_thrust_label = QLabel("Lower Thrust: ")
        lower_thrust_input = QLineEdit()

        upper_thrust_label = QLabel("Upper Thrust: ")
        upper_thrust_input = QLineEdit()

        maxthrust_precent_label = QLabel("Max Thrust %: ")
        maxthrust_precent_input = QLineEdit()

        spacing_label = QLabel("Spacing: ")
        spacing_input = QLineEdit()

        #Make inputs visible
        layout.addRow(lower_thrust_label, lower_thrust_input)
        layout.addRow(upper_thrust_label, upper_thrust_input)
        layout.addRow(maxthrust_precent_label, maxthrust_precent_input)
        layout.addRow(spacing_label, spacing_input)

        #Add submit values button
        button_layout = QHBoxLayout()
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(submit)
        button_layout.addWidget(submit_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        window.setLayout(main_layout)

        window.show()

        sys.exit(app.exec())

    if __name__ == "__main__":
        main()