import scipy.io
import pandas as pd
import os

# Load the MAT file
file_path = 'F:/SEED-VIG/SEED-VIG/EEG_Feature_5Bands/1_20151124_noon_2.mat'
mat = scipy.io.loadmat(file_path)

# Extract the 'de_LDS' variable
de_LDS = mat['de_LDS']

# Define the frequency bands
frequency_bands = ['1-4', '4-8', '8-14', '14-31', '31-50']

# Base path for saving CSV files
base_path = 'F:/SEED-VIG数据集/9.提取DE/1/'

# Check if the base directory exists, if not, create it
if not os.path.exists(base_path):
  os.makedirs(base_path)

# Create CSV files for each frequency band
for freq_index, freq_band in enumerate(frequency_bands):
  # Create a directory for the frequency band if it doesn't exist
  directory_path = os.path.join(base_path, freq_band)
  os.makedirs(directory_path, exist_ok=True)

  # Iterate over time segments
  for time_segment in range(de_LDS.shape[1]):
    # Extract data for the current time segment and frequency band
    data = de_LDS[:, time_segment, freq_index]

    # Create a DataFrame with channels and DE columns swapped
    df = pd.DataFrame({'channels': range(1, 18), 'DE': data})

    # Save to CSV
    csv_file_path = os.path.join(directory_path, f'time_segment_{time_segment+1}.csv')
    df.to_csv(csv_file_path, index=False)

# Inform the user that the process is complete
completed_path = base_path
completed_path