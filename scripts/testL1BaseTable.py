import pandas as pd

# Path to the CSV file
file_path = '$HOME/sta/L1Base_Evo/l1bbase_data_export.csv'

# Read the CSV file
data = pd.read_csv(file_path)

# Display the first few rows of the data
print(data.head())