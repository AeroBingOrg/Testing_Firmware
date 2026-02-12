from LoadCellMath import Load_cell_math
from LoadCellGraph import testing_UI
import tkinter as tk
from tkinter import messagebox
import os
  
def main():
  # Create main window
  root = tk.Tk()
  root.title("Input Values")
  root.geometry("300x200")
   
  # Variables to store values
  lowerthrust = tk.IntVar()
  upperthrust = tk.IntVar()
  maxthrust_precent = tk.IntVar()
  spacing = tk.IntVar()
 
  # Create input fields
  tk.Label(root, text="lowerthrust:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
  tk.Entry(root, textvariable=lowerthrust).grid(row=0, column=1, padx=10, pady=5)
    
  tk.Label(root, text="upperthrust:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
  tk.Entry(root, textvariable=upperthrust).grid(row=1, column=1, padx=10, pady=5)
    
  tk.Label(root, text="maxthrust_precent:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
  tk.Entry(root, textvariable=maxthrust_precent).grid(row=2, column=1, padx=10, pady=5)
    
  tk.Label(root, text="spacing:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
  tk.Entry(root, textvariable=spacing).grid(row=3, column=1, padx=10, pady=5)
    
  # Function to save values
  def run():
    values = {
      'lowerthrust': lowerthrust.get(),
      'upperthrust': upperthrust.get(),
      'maxthrust_precent': maxthrust_precent.get(),
      'spacing': spacing.get()
    }

    try:
      print(Load_cell_math(values["lowerthrust"]))
    except: 
      print("lowerthrust fail")

    try:
      print(Load_cell_math(values["upperthrust"]))
    except: 
      print("upperthrust fail")

    try:
      print(Load_cell_math(values["maxthrust_precent"]))
    except: 
      print("maxthrust_precent fail")

    try:
      print(Load_cell_math(values["spacing"]))
    except: 
      print("spacing fail")


    try:
      math = Load_cell_math(values['lowerthrust'], values["upperthrust"], values["maxthrust_precent"], values["spacing"])

      filtered_pressure_above_20N, filtered_thrust_above_20N, filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N = math.calculations()

      testing_UI.plots(filtered_pressure_above_20N, filtered_thrust_above_20N, 
                       filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N)

            
    except:
      messagebox.showerror("Error","Failed Calculations & Graphing")

    root.destroy()
    
  tk.Button(root, text="Import Values", command=run).grid(row=4, column=0, columnspan=2, pady=20)

  root.mainloop()
  
  tk.Button(root, text="Save & Run", command=run).grid(row=4, column=0, columnspan=2, pady=20)
    
  root.mainloop()

if __name__ == "__main__":
  main()