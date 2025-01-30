import csv

def process_readings(input_file, output_file):
    try:
        # Open the input file for reading and output file for writing
        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Read the header
            header = next(reader)
            writer.writerow(header)  # Write the header to the output file
            
            # Initialize accumulators
            accumulated = [0] * len(header)  # To store accumulated values for all columns
            time_diff_index = header.index("Time_Diff")  # Index of Time_Diff column
            time_accumulated = 0.0  # Accumulator for Time_Diff

            for row in reader:
                # Convert numeric fields to float
                numeric_row = [float(value) if i != 0 else value for i, value in enumerate(row)]
                
                # Add values to the accumulator
                for i in range(1, len(header)):  # Skip the Timestamp column
                    accumulated[i] += numeric_row[i]
                
                time_accumulated += numeric_row[time_diff_index]

                # Check if time accumulated exceeds 1 millisecond
                if time_accumulated >= 0.001:  # 1 millisecond
                    accumulated[time_diff_index] = time_accumulated
                    writer.writerow(accumulated)
                    
                    # Reset accumulators
                    accumulated = [0] * len(header)
                    accumulated[0] = numeric_row[0]  # Retain the Timestamp
                    time_accumulated = 0.0

    except Exception as e:
        print(f"Error: {e}")

# Input and output file paths
input_file = "perf_data_readings.txt"
output_file = "merged_readings.txt"

# Call the function
process_readings(input_file, output_file)
