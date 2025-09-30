import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os

class Load_cell_math:
  def __init__(self, lowerthrust: int, upperthrust: int, maxthrust_precent: int, spacing: int):
    self.lowerthrust = lowerthrust
    self.upperthrust = upperthrust
    self.maxthrust_precent = maxthrust_precent
    self.spacing = spacing
    
  def calculations(self):
    # Load CSV data file
    filepath = filedialog.askopenfilename(
        initialdir="/",  
        title="Select a file",  
        filetypes=(
            ("CSV files", "*.csv")
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

    # Getting user input Variables
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    MaxThrust = simpledialog.askstring("Input", "What is the expected max thrust (in Newtons):", initialvalue="0")
    
    if MaxThrust is None:
        return
    try:
        # Convert the user input to the desired variable type
        MaxThrustInput = float(MaxThrust)
        TooLarge = MaxThrustInput * self.maxthrust_precent
    except ValueError:
        messagebox.showerror("Error", "Invalid input for max thrust")
        return

    # Getting Data
    # Extract time (first column), thrust (third column), and pressure (fifth column) data
    time_sec = dataTable.iloc[:, 0].values 
    thrust_N = dataTable.iloc[:, 2].values  
    pressure_psi = dataTable.iloc[:, 4].values
    L = len(thrust_N)

    time_ms = time_sec / 1000  

    # Find indices where thrust is greater than upperthrust and drops below lowerthrust
    indices_above_20N = np.where(thrust_N > self.upperthrust)[0]
    indices_below_20N = np.where(thrust_N < self.lowerthrust)[0]
    
    IAL = len(indices_above_20N)
    IBL = len(indices_below_20N)

    # Process indices to remove outliers
    indices_above_20Nfixed = []
    
    for i in range(IAL):
        k = indices_above_20N[i]
        
        # Make sure we don't go out of bounds
        start_idx = max(0, k - self.spacing)
        end_idx = min(L, k + self.spacing + 1)
        
        iThrustData = thrust_N[start_idx:end_idx]
        DumbBig = thrust_N[k]
        
        if DumbBig > TooLarge:
            continue
        
        # Calculate differences
        diffthrust = np.diff(iThrustData)
        
        if len(diffthrust) > 0 and np.max(diffthrust) > 1000:
            continue
        
        # Calculate average
        iAvg = np.mean(iThrustData)
        
        if iAvg > 20:
            indices_above_20Nfixed.append(indices_above_20N[i])

    indices_above_20Nfixed = np.array(indices_above_20Nfixed)

    if len(indices_above_20Nfixed) == 0:
        messagebox.showwarning("warning",'There were not enough data points to gather data now displaying the max pressure and thrust recorded')
        if len(indices_above_20N) > 0:
            max_idx = indices_above_20N[-1]
            messagebox(f'Max Thrust: {thrust_N[max_idx]:.2f} N, Max Pressure: {pressure_psi[max_idx]:.2f} psi')
        return

    # Check if the thrust drops below lowerthrust in the data
    if len(indices_below_20N) > 0:
        # Select points around when thrust exceeds upperthrust
        start_A20N = max(indices_above_20Nfixed[0] - self.spacing, 0)
        end_index_A20N = min(indices_above_20Nfixed[0] + self.spacing, L - 1)

        # Process end indices
        LDB2 = indices_above_20Nfixed[-1]
        BeginNew2 = LDB2 + 1
        TimeofBurn = time_ms[indices_above_20Nfixed[-1]] - time_ms[indices_above_20Nfixed[0]]
        end_A20N = min(LDB2 + 200, len(thrust_N) - 1)

        # Filtered data based on conditions
        filtered_time_above_20N = time_ms[start_A20N:end_A20N+1]
        filtered_thrust_above_20N = thrust_N[start_A20N:end_A20N+1]
        filtered_pressure_above_20N = pressure_psi[start_A20N:end_A20N+1]

        # Calculate Impulse (Riemann sum of thrust)
        if len(filtered_time_above_20N) > 1:
            dt = np.diff(filtered_time_above_20N)  # Calculate time intervals
            impulse = np.sum(filtered_thrust_above_20N[:-1] * dt)  # Riemann sum calculation
        else:
            impulse = 0

    return filtered_pressure_above_20N, filtered_thrust_above_20N, filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N