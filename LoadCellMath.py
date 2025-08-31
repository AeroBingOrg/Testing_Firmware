import pandas as df
import numpy as np
import math

class Load_cell_math:
  def __init__(self, lowerthrust, upperthrust, maxthrustpercent, spacing, maxthrust):
    self.lowerthrust = lowerthrust
    self.upperthrust = upperthrust
    self.maxthrustpercent = maxthrustpercent
    self.spacing = spacing
    self.maxthrust = maxthrust

  def get_data(self, df_map):
    sec_data = df_map['s']
    thrust_N = df_map['thrust']
    ms_data = sec_data / 1000
    toolarge = self.maxthrust * self.maxthrustpercent

    indices_above_20N = thrust_N > self.upperthrust
    indices_below_20N = thrust_N < self.lowerthrust

    IAL = len(indices_above_20N)
    IBL = len(indices_below_20N)

    for i in range(IAL):
      k = indices_above_20N[i]
      iThrustData = thrust_N[k-self.Spacing:k+self.Spacing]

      ITDlen = len(iThrustData)
      DumbBig = thrust_N[k]
      if DumbBig > toolarge:
        iThrustData.remove[DumbBig]
      
      if not iThrustData[i-1] == None:
        if abs(iThrustData[i-1] - k) > 1000:
          iThrustData.remove(k)

      