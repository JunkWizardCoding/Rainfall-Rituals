# -*- coding: utf-8 -*-
"""
@author: Merlin <|:3
"""
import pandas as pd
import matplotlib.pyplot as plt
import os  # operating system dependent functionality
import glob  # finds all the pathnames matching a specified pattern
import re    # Regex for extracting year

# Define threshold for a "heavy rain day" in l/m²
# CHANGE THIS VARIABLE TO SUIT YOUR NEEDS
RainyDayCutoff = 5

# Define column names
colnames = ['Date', 'Rainfall_L_per_m2']
df_list = []  # List to store individual DataFrames

# Define data directory, read data, extract weekday, full date, and year from filename
for filename in glob.glob("D:\\Rainfall-Data\\Data\\Muenchen-Stadt\\*.csv"):
    temp_df = pd.read_csv(filename, names=colnames, header=0, engine='python')

    # Extract year from filename (e.g., "Muenchen_Stadt_1982T3.csv" → "1982")
    year_match = re.search(r'(\d{4})', filename)
    if year_match:
        extracted_year = year_match.group(1)
        temp_df['Year'] = int(extracted_year)  # Convert to integer

    # Extract weekday initials and the actual date part
    temp_df['Weekday'] = temp_df['Date'].str.extract(r'(^\w{2})')  # First two letters (Weekday)
    temp_df['Date'] = temp_df['Date'].str.extract(r'(\d{2}\.\d{2}\.)')  # Extract only the date part

    # Merge "Date" and "Year" into a full date (e.g., "01.01." + "1982" → "01.01.1982")
    temp_df['Full_Date'] = temp_df['Date'] + extracted_year

    # Convert to datetime format (e.g., "01.01.1982" → 1982-01-01)
    temp_df['Full_Date'] = pd.to_datetime(temp_df['Full_Date'], format='%d.%m.%Y', errors='coerce')

    # Remove erroneous rainfall data (negative values)
    temp_df = temp_df[temp_df['Rainfall_L_per_m2'] >= 0]

    df_list.append(temp_df)

# Concatenate all DataFrames into one
df_final = pd.concat(df_list, ignore_index=True)

# Display first few rows to check
print(df_final.head())

# Get min and max year from df_final
min_year = df_final['Year'].min()
max_year = df_final['Year'].max()

# Count how many times rainfall was greater than RainyDayCutoff per weekday
df_rainy_days = df_final[df_final['Rainfall_L_per_m2'] > RainyDayCutoff].groupby('Weekday', as_index=False).size()

# Define the correct weekday order
weekday_order = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

# Convert Weekday to categorical type with defined order and sort
df_rainy_days['Weekday'] = pd.Categorical(df_rainy_days['Weekday'], categories=weekday_order, ordered=True)
df_rainy_days = df_rainy_days.sort_values('Weekday')

# Plot the data
plt.style.use('dark_background')
plt.figure(figsize=(8, 6))
plt.bar(df_rainy_days['Weekday'], df_rainy_days['size'], color='deepskyblue', edgecolor='black', linewidth=0.8)
plt.xlabel('Weekday')
plt.ylabel(f'Number of Rainy Days (>{RainyDayCutoff} L/m²)')
plt.title(f'Number of Rainy Days per Weekday ({min_year}–{max_year})')
plt.grid(visible=True, color='gray', linestyle='--', linewidth=1, alpha=0.5)
plt.tight_layout()

# Save the figure to the "graphs" folder with a clean filename based on the Y-label and year range
output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

# Extract clean label by removing parentheses and their content, then strip and replace spaces with underscores
raw_ylabel = plt.gca().get_ylabel()
clean_ylabel = re.sub(r'\s*\([^)]*\)', '', raw_ylabel).strip().replace(' ', '_')

# Construct and save the figure filename
filename = f"{clean_ylabel}_{min_year}-{max_year}.png"
output_path = os.path.join(output_dir, filename)
plt.savefig(output_path, dpi=300)

print(f"Graph saved as: {output_path}")

plt.show()