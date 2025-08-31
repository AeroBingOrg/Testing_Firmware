import numpy as np
import pandas as pd
import streamlit as st

class testing_UI:
  def __init__(self):
    self.df_map = {}
    self.df = None
    self.root = None

  def csv_loader(self, uploaded_file):
    """function for loading csv data and making it into a hash map"""
    try: 
      if self.uploaded_file is None:
        st.error("No CSV data loaded")
        return False
      else:
        self.df = pd.read_csv(uploaded_file)
        self.df_map = {}  # Clear previous data
        for col in self.df.columns:
          self.df_map[col] = self.df[col]
        return self.df_map
          
    except Exception as e:
      st.error(f"Failed to load CSV: {str(e)}")
      return False
    
  def UI_display(self):
    """UI Display for loading csv and displaying data"""
    st.title("Testing UI")
    st.header("Load Cell UI")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
    if uploaded_file is not None:
      if self.csv_loader(uploaded_file):
        st.success("CSV file loaded successfully!")
                
        st.subheader("Data Preview")
        st.dataframe(self.df)

def main():
  app = testing_UI()
  app.UI_display()

if __name__ == "__main__":
  main()