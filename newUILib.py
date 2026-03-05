from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QMessageBox
import sys
import traceback
import os

class Window(QWidget):
    
    def main(): 

        def submit(): #this runs when you submit your values
            #os.system('cls')
            values = {
            'lowerthrust': float(lower_thrust_input.text()),
            'upperthrust': float(upper_thrust_input.text()),
            'maxthrust_precent': float(maxthrust_precent_input.text()),
            'spacing': int(spacing_input.text())
            }

            try:
                math = Load_cell_math(values['lowerthrust'], values["upperthrust"], values["maxthrust_precent"], values["spacing"])

                filtered_pressure_above_20N, filtered_thrust_above_20N, filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N = math.calculations()

                graph = testing_UI()
                graph.plots(filtered_pressure_above_20N, filtered_thrust_above_20N, 
                       filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N)
                
                
            except Exception as e:
                print(f"Basic error:\n {e} \n")
                print("Advanced error log: ")
                traceback.print_exc()
                QMessageBox.information(window, "Error", "Failed Calculations & Graphing.")

        app = QApplication(sys.argv)
        
        #Create window
        window = QWidget()
        window.resize(350,200)
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

        #make entire UI visible
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        window.setLayout(main_layout)

        window.show()

        sys.exit(app.exec())

    if __name__ == "__main__":
        main()