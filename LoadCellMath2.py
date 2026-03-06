import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os

class Load_cell_math:
  def __init__(self, min_pressure: float):
    self.min_pressure = min_pressure

  def calculations(self):
    # Load CSV data file
    filepath = filedialog.askopenfilename(
        initialdir="/",  
        title="Select a file",  
        filetypes=(
            ("CSV Files", "*.csv"), ('All', '*.*')
        )
    )

    try:
        # Read the data from the CSV file
        dataTable = pd.read_csv(filepath, skiprows=1)  # Skip the first row if it contains headers
    except FileNotFoundError:
        messagebox.showerror("Error", "File Not Found")
        return
    except Exception as e:
        messagebox.showerror("Error", "Error Loading File")
        return

    # Getting Data
    # Extract time (first column), thrust (third column), and pressure (fifth column) data
    
    #Gets rid of rows where pressure < input min_pressure
    dataTable = dataTable[dataTable.iloc[:,4] > self.min_pressure]
    dataTable.reset_index(drop=True)

    time_ms = dataTable.iloc[:, 0].values 
    thrust_N = dataTable.iloc[:, 2].values  
    pressure_psi = dataTable.iloc[:, 4].values

    time_sec = time_ms / 1000

    '''Debug prints
    print(f"time: {time_sec}")
    print(f"Thrust: {thrust_N}")
    print(f"pressure: {pressure_psi}")

    print(f"csv: {dataTable}") '''

        # Calculate Impulse (Riemann sum of thrust)
    if len(time_sec) > 1:
        dt = np.diff(time_sec)  # Calculate time intervals
        impulse = np.sum(thrust_N[:-1] * dt)  # Riemann sum calculation
    else:
        impulse = 0
    

    return pressure_psi, thrust_N, time_sec, impulse, time_ms, 0, len(dataTable)-1