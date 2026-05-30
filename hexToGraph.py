# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# FREQUENCY = "4"

# # Define file path
# # file_path = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.10.txt"
# # file_path = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.20.txt"
# file_path = f"../Testing/Experiment-2/output_hex_data_192.168.1.40.txt"

# # Read hex data from text file
# data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)  

# # Extract first and second 16-bit parts
# first_16_bits = data[0] + data[1]  # Concatenate first two hex values

# # Convert hex to decimal and interpret as signed 16-bit integers
# decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

# # Convert to -5V to 5V scale
# voltage_values = (decimal_values / 32767) * 5  # Convert to voltage range

# # Generate time values (assuming 200 ns per step)
# time_step = 200e-9  # 200 nanoseconds
# time_values = np.arange(len(voltage_values)) * time_step  # Time axis

# # Apply moving average filter
# window_size = 1  # Adjust as needed
# smoothed_values = np.convolve(voltage_values, np.ones(window_size)/window_size, mode='valid')

# # Adjust `time_values` to match the new length of `smoothed_values`
# time_values = time_values[:len(smoothed_values)]  

# # Plot the smoothed data
# plt.figure(figsize=(12, 6))
# plt.plot(time_values, smoothed_values, '-',color = 'orange', linewidth=1.5)
# plt.title("Smoothed 16-bit Values Converted to Voltage (-5V to 5V) over Time - Board 1")


# # plt.plot(time_values, smoothed_values, '-',color = 'green', linewidth=1.5)
# # plt.title("Smoothed 16-bit Values Converted to Voltage (-5V to 5V) over Time - Board 2")

# plt.xlabel("Time (seconds)")
# plt.ylabel("Voltage (V)")
# plt.grid(True)

# # Set y-axis range for -5V to 5V
# plt.ylim([-5, 5]) 
# plt.xlim([0, 3])

# # Show the plot  
# plt.show()



######################################################################################################### Trigger

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Constants
# FREQUENCY = "5000"
# time_step = 200e-9  # 200 nanoseconds per step

# # Define file path
# file_path = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.30.txt"

# try:
#     # Read hex data from text file
#     data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)

#     # Extract first and second 16-bit parts
# # # Extract first and second 16-bit parts
#     first_16_bits = data[0] + data[1]  # Concatenate first two hex values

#     # Convert hex to decimal and interpret as signed 16-bit integers
#     decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

#     # Convert to -5V to 5V scale
#     voltage_values = (decimal_values / 32767) * 5  # Convert to voltage range

#     # Generate time values (assuming 200 ns per step)
#     time_step = 200e-9  # 200 nanoseconds
#     time_values = np.arange(len(voltage_values)) * time_step  # Time axis

#     # Apply moving average filter
#     window_size = 1  # Adjust as needed
#     smoothed_values = np.convolve(voltage_values, np.ones(window_size)/window_size, mode='valid')

#     # Adjust `time_values` to match the new length of `smoothed_values`
#     time_values = time_values[:len(smoothed_values)]  

#     # Extract the 15th bit

#     # Plot the original voltage signal
#     plt.figure(figsize=(12, 6))
#     plt.plot(time_values, smoothed_values, '-', color='orange', linewidth=1.5, label="Voltage Signal")

#     plt.title("Voltage Signal and 15th Bit Representation")
#     plt.xlabel("Time (seconds)")
#     plt.ylabel("Voltage (V)")
#     plt.grid(True)
#     plt.ylim([-5, 5])  # Adjust for better visibility of 15th bit signal
#     plt.xlim(0,5)  # Adjust for better visibility of 15th bit signal
#     plt.legend()
    
#     # Show the plot
#     plt.show()

# except FileNotFoundError:
#     print(f"⚠️ File not found: {file_path}")
# except Exception as e:
#     print(f"Error processing the file: {e}")



###########################################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

FREQUENCY = "5000"  # Set desired frequency (change as needed)
dataset_index="450"
# Define base directory
base_dir = f""

# Define board files with corresponding colors
board_files = {
    "Board1": {"path": f"Board_1_{dataset_index}_KHz.txt", "color": "orange"},
    # "Board2": {"path": f"{base_dir}output_hex_data({FREQUENCY}Khz)_192.168.1.20.txt", "color": "green"},
    # "Board3": {"path": f"{base_dir}output_hex_data({FREQUENCY}Khz)_192.168.1.30.txt", "color": "red"},
    # "Board4": {"path": f"{base_dir}output_hex_data({FREQUENCY}Khz)_192.168.1.40.txt", "color": "blue"},
}

# Output directory for saving graphs
output_dir = f"../Testing/Figures/Freq/{FREQUENCY}Khz/"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Loop through both boards and create separate plots
for board_name, info in board_files.items():
    file_path = info["path"]
    color = info["color"]

    if os.path.isfile(file_path):
        print(f"✅ Processing: {file_path}")

        # Read hex data from text file
        data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)

        # Extract first and second 16-bit parts
        first_16_bits = data[0] + data[1]  # Concatenate first two hex values

        # Convert hex to decimal and interpret as signed 16-bit integers
        decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

        # Convert to -5V to 5V scale
        voltage_values = (decimal_values / 32767) * 5  # Convert to voltage range

        # Generate time values (assuming 200 ns per step)
        time_step = 200e-9  # 200 nanoseconds
        time_values = np.arange(len(voltage_values)) * time_step  # Time axis

        # Apply moving average filter
        window_size = 1  # Adjust as needed
        smoothed_values = np.convolve(voltage_values, np.ones(window_size)/window_size, mode='valid')

        # Adjust `time_values` to match the new length of `smoothed_values`
        time_values = time_values[:len(smoothed_values)]
        # smoothed_values = smoothed_values[15000000:25000000]
        # time_values = time_values[15000000:25000000]

        # Create a separate plot for each board
        plt.figure(figsize=(12, 6))
        plt.plot(time_values, smoothed_values, '-', color=color, linewidth=1.5, label=board_name)

        plt.title(f"Smoothed 16-bit Values Converted to Voltage (-5V to 5V) - {board_name} at {FREQUENCY} kHz")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Voltage (V)")
        plt.grid(True)
        plt.ylim([-5, 5])
        plt.legend()

        # # Save the plot separately
        # output_file = f"{output_dir}{FREQUENCY}_B_{board_name}.png"
        # plt.savefig(output_file, dpi=300)
        # plt.close()  # Close figure to prevent display
        

        plt.show()


    else:
        print(f"⚠️ File not found: {file_path}")
# Compute autocorrelation (normalized)
   
