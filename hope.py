import pandas as pd
import re

# Define the event types to extract
event_types = [
    "L1-dcache-loads", "L1-dcache-stores", "L1-icache-load-misses",
    "LLC-loads", "LLC-load-misses", "LLC-stores", "LLC-store-misses",
    "dTLB-loads", "dTLB-load-misses", "dTLB-stores", "dTLB-store-misses",
    "iTLB-load-misses", "branch-loads", "branch-load-misses"
]

# File names
input_file = "perf_data.txt"
output_file = "perf_data_readings.txt"

# Function to process a chunk
def process_chunk(chunk):
    data = []
    for line in chunk:
        match = re.search(r'(\d+\.\d+):\s+(\d+)\s+cpu_core/([A-Za-z0-9\-_]+)/', line)
        if match:
            timestamp = float(match.group(1))
            count = int(match.group(2))
            event = match.group(3)
            if event in event_types:
                data.append((timestamp, event, count))
    return data

# Initialize storage for final data
final_data = []

# Read and process file in chunks
chunk_size = 100000  # Number of lines per chunk
with open(input_file, 'r') as file:
    chunk = []
    for i, line in enumerate(file):
        chunk.append(line)
        if i % chunk_size == 0 and i > 0:
            processed = process_chunk(chunk)
            final_data.extend(processed)
            chunk = []
    # Process remaining lines
    if chunk:
        processed = process_chunk(chunk)
        final_data.extend(processed)

# Convert to pandas DataFrame for structured processing
df = pd.DataFrame(final_data, columns=["Timestamp", "Event", "Count"])

# Pivot the data to have events as columns
pivot_df = df.pivot_table(index="Timestamp", columns="Event", values="Count", fill_value=0)

# Add derived metrics
pivot_df = pivot_df.reset_index()
pivot_df["Elapsed_Time"] = pivot_df["Timestamp"] - pivot_df["Timestamp"].iloc[0]
pivot_df["Time_Diff"] = pivot_df["Elapsed_Time"].diff().fillna(0)
pivot_df["Timestamp_Normalized"] = pivot_df["Timestamp"] / pivot_df["Timestamp"].max()

# Save to output file
pivot_df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}.")
