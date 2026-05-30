

import struct
import sys

def bin_to_hex(input_file, output_file):
    """Converts a binary file to a hexadecimal text file."""
    try:
        # Open the input file in binary read mode and output file in text write mode
        with open(input_file, "rb") as bin_file, open(output_file, "w") as txt_file:
            while True:
                # Read 1024 uint32 values (each 4 bytes) at a time
                chunk = bin_file.read(1024 * 4)  # Read in 4-byte blocks (uint32)
                
                # Break if end of file
                if not chunk:
                    break

                # Convert binary data to a list of uint32 (big-endian)
                uint32_values = struct.unpack(">" + "I" * (len(chunk) // 4), chunk)

                # Process each uint32 value
                for value in uint32_values:
                    # Convert uint32 to hex (8 characters, zero-padded)
                    hex_str = f"{value:08x}"
                    # Format with spaces (e.g., "00 00 00 01")
                    formatted_hex = " ".join([hex_str[i:i+2] for i in range(0, 8, 2)])
                    # Write to output file
                    txt_file.write(formatted_hex + "\n")

        print(f"Conversion completed. Hexadecimal data saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bin_to_hex.py <input_binary_file> <output_text_file>")
    else:
        bin_to_hex(sys.argv[1], sys.argv[2])
