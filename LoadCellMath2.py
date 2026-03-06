import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os

class Load_cell_math:
  def __init__(self, lowerthrust: float, upperthrust: float, maxthrust_precent: float, spacing: int):
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

    # Getting user input Variables
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    MaxThrust = float(simpledialog.askstring("Input", "What is the expected max thrust (in Newtons):", initialvalue="0"))
    
    if MaxThrust is None:
        return None, None, None, None, None, None, None
    try:
        # Convert the user input to the desired variable type
        MaxThrustInput = MaxThrust
        TooLarge = (MaxThrustInput) * float(self.maxthrust_precent) #1000000
    except ValueError:
        messagebox.showerror("Error", "Invalid input for max thrust")
        return None, None, None, None, None, None, None

    # Getting Data
    # Extract time (first column), thrust (third column), and pressure (fifth column) data
    dataTable = dataTable[dataTable.iloc[:,4] > 10]
    dataTable.reset_index(drop=True)

    time_ms = dataTable.iloc[:, 0].values 
    thrust_N = dataTable.iloc[:, 2].values  
    pressure_psi = dataTable.iloc[:, 4].values
    L = len(thrust_N)

    time_sec = time_ms / 1000  

    print(f"time: {time_sec}")
    print(f"Thrust: {thrust_N}")
    print(f"pressure: {pressure_psi}")

    print(f"csv: {dataTable}")
    # Find indices where thrust is greater than upperthrust and drops below lowerthrust
    #indices_above_20N = np.argwhere(thrust_N > self.upperthrust)
    #indices_below_20N = np.argwhere(thrust_N < self.lowerthrust)
    '''
    indices_above_20N = np.array([i for i in thrust_N if i > self.upperthrust],dtype=int)
    indices_below_20N = np.array([i for i in thrust_N if i < self.lowerthrust],dtype=int)

    print(f"Above 20: {thrust_N[indices_above_20N]}")
    print(f"Below 20: {thrust_N[indices_below_20N]}")

    IAL = len(indices_above_20N)
    IBL = len(indices_below_20N)


    # Process indices to remove outliers (not a perfect method but the original filter was not working)
    indices_above_20Nfixed = []

    #array of z scores for each data point
    z_scores = zscore(thrust_N)

    #filters out points whose z score is large
    indices_above_20Nfixed = np.argwhere(np.array(thrust_N[np.abs(z_scores) <= 3]))

    for i in range(IAL): old outlier filter
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
            messagebox.showinfo(f'Max Thrust: {thrust_N[max_idx]:.2f} N, Max Pressure: {pressure_psi[max_idx]:.2f} psi') #this displays all the info in the title of the window so it might get cut off
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
        '''
        # Calculate Impulse (Riemann sum of thrust)
    if len(time_ms) > 1:
        dt = np.diff(time_sec)  # Calculate time intervals
        impulse = np.sum(thrust_N[:-1] * dt)  # Riemann sum calculation
    else:
        impulse = 0
    

    return pressure_psi, thrust_N, time_ms, impulse, time_sec, 0, len(dataTable)-1