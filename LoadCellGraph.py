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
    ax1.text(0.02, 0.98, f'Max Thrust: {max_thrust:.2f} N', 
            ha='left', va='top', color='red', fontsize=10)

    # Display Impulse
    ax1.text(0.02, 0.85, f'Impulse: {impulse:.2f} Ns', 
            ha='left', va='top', color='blue', fontsize=10)

    # Display Burn Time
    timeBurn = time_ms[end_A20N] - time_ms[start_A20N]
    ax1.text(0.02, 0.72, f'Burn Time: {timeBurn:.2f} s', 
            transform=ax1.transAxes, ha='left', va='top', 
            color='green', fontsize=10)

    # Pressure plot
    ax2.plot(filtered_time_above_20N, filtered_pressure_above_20N, '-')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Pressure (psi)')
    ax2.set_title('Time vs. Pressure')
    ax2.grid(True)

    # Display maximum pressure value
    max_pressure = np.max(filtered_pressure_above_20N)
    ax2.text(0.02, 0.98, f'Max Pressure: {max_pressure:.2f} psi', 
            ha='left', va='top', color='red', fontsize=10)

    plt.tight_layout()
    plt.show()