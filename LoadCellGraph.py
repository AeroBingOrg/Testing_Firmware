import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

class testing_UI:
  def plots(self, filtered_pressure_above_20N, filtered_thrust_above_20N, filtered_time_above_20N, impulse, time_ms, end_A20N, start_A20N):
    # Plot time vs. thrust and pressure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Thrust plot
    ax1.plot(filtered_time_above_20N, filtered_thrust_above_20N, '-')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Thrust (N)')
    ax1.set_title('Time vs. Thrust')
    ax1.grid(True)

    # Display maximum thrust value in the top left corner
    max_thrust = np.max(filtered_thrust_above_20N)
    ax1.text(0.98, 0.98, f'Max Thrust: {max_thrust:.2f} N', transform=ax1.transAxes,
            ha='right', va='top', color='red', fontsize=10)

    # Display Impulse
    ax1.text(0.98, 0.85, f'Impulse: {impulse:.2f} Ns', transform=ax1.transAxes,
            ha='right', va='top', color='blue', fontsize=10)

    #Find first instance where pressure > 90, and last instance where pressure > 90
    boolean_column = filtered_pressure_above_20N >= 90
    differences = np.diff(boolean_column.astype(int))

    start_90psi = np.where(differences == 1)[0] + 1
    end_90psi = np.where(differences == -1)[0]

    # Display Burn Time
    timeBurn = abs(filtered_time_above_20N[start_90psi] - filtered_time_above_20N[end_90psi])
    ax1.text(0.98, 0.72, f'Burn Time: {timeBurn.item():.2f} s', 
            transform=ax1.transAxes, ha='right', va='top', 
            color='green', fontsize=10)
    
    # Pressure plot
    ax2.plot(filtered_time_above_20N, filtered_pressure_above_20N, '-')

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Pressure (psi)')
    ax2.set_title('Time vs. Pressure')
    ax2.grid(True)

    # Display maximum pressure value
    max_pressure = np.max(filtered_pressure_above_20N)
    ax2.text(0.98, 0.98, f'Max Pressure: {max_pressure:.2f} psi', transform=ax2.transAxes,
            ha='right', va='top', color='red', fontsize=10)

    plt.style.use('seaborn-v0_8')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.show()