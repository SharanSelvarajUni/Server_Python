import subprocess

def run_script(script_name, *args):
    """ Executes a Python script with optional arguments and prints its output."""
    try:
        result = subprocess.run(["python", script_name, *args], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"Error executing {script_name}: {e}") 

# Define script file names
conversion_script = "binToHex.py"  # Script that converts binary to hex
after_conversion_script = "synchronizationAnalysis.py"  # Script that analyzes synchronization
dataset_index= "500"
# FREQUENCY= "120"
# Define input and output file names
bin_input_file_1 = f"Board_1_{dataset_index}_KHz.bin"
# bin_input_file_2 = f"../Testing/Experiment-1/{FREQUENCY}Khz/ClientData_192.168.1.20.bin"
# bin_input_file_3 = f"../Testing/Experiment-1/{FREQUENCY}Khz/ClientData_192.168.1.30.bin"
# bin_input_file_4 = f"../Testing/Experiment-1/{FREQUENCY}Khz/ClientData_192.168.1.40.bin"
hex_output_file_1 = f"Board_1_{dataset_index}_KHz.txt"
# hex_output_file_2 = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.20.txt"
# hex_output_file_3 = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.30.txt"
# hex_output_file_4 = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.40.txt"
# sync_output_file = f"../Testing/Experiment-1/{FREQUENCY}Khz/synchronization_analysis.txt"
# sync_output_file = f"../Testing/Experiment-1/Analysis_Results"

# Execute binary to hex conversion for both files
print("Running Binary to Hex Conversion for first file...")
run_script(conversion_script, bin_input_file_1 , hex_output_file_1)

print("Running Binary to Hex Conversion for second file...")
# run_script(conversion_script, bin_input_file_2, hex_output_file_2)

print("Running Binary to Hex Conversion for third file...")
# run_script(conversion_script, bin_input_file_3, hex_output_file_3)
print("Running Binary to Hex Conversion for fourth file...")
# run_script(conversion_script, bin_input_file_4, hex_output_file_4)

# print(f"Hex data saved to: {hex_output_file_1}, {hex_output_file_2}, {hex_output_file_3} and {hex_output_file_4}")

# Run synchronization analysis after conversion
# print("Running Synchronization Analysis...")
# run_script(after_conversion_script, hex_output_file_1, hex_output_file_2, sync_output_file)

# print(f"Synchronization analysis saved to: {sync_output_file}")

print("All tasks completed successfully.")
