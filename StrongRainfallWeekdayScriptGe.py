# -*- coding: utf-8 -*-
"""
@author: Merlin <|:3
"""
import pandas as pd
import matplotlib.pyplot as plt
import os # operating system dependent functionality
import glob # finds all the pathnames matching a specified pattern
import re  # Regex for extracting year


# Define threshold for a "heavy rain day" in l/m²
# CHANGE THIS VARIABLE TO SUIT YOUR NEEDS
RainyDayCutoff = 5


# Define column names
colnames = ['Datum', 'Niederschlag_in_Liter_pro_m²']
df_list = []  # List to store individual DataFrames

# Define data directory, read data, extract weekday, full date, and year from filename
for filename in glob.glob("D:\\Rainfall-Data\\Data\\Muenchen-Stadt\\*.csv"):
    temp_df = pd.read_csv(filename, names=colnames, header=0, engine='python')
    
    # Extract year from filename (e.g., "Muenchen_Stadt_1982T3.csv" → "1982")
    year_match = re.search(r'(\d{4})', filename)
    if year_match:
        extracted_year = year_match.group(1)
        temp_df['Jahr'] = int(extracted_year)  # Convert to integer
    
    # Extract weekday initials and the actual date part
    temp_df['Wochentag'] = temp_df['Datum'].str.extract(r'(^\w{2})')  # First two letters (Weekday)
    temp_df['Datum'] = temp_df['Datum'].str.extract(r'(\d{2}\.\d{2}\.)')  # Extract only the date part
    
    # Merge "Datum" and "Jahr" into a full date (e.g., "01.01." + "1982" → "01.01.1982")
    temp_df['Vollständiges_Datum'] = temp_df['Datum'] + extracted_year
    
    # Convert to datetime format (e.g., "01.01.1982" → 1982-01-01)
    temp_df['Vollständiges_Datum'] = pd.to_datetime(temp_df['Vollständiges_Datum'], format='%d.%m.%Y', errors='coerce')
    
    # Remove erroneous rainfall data (negative values)
    temp_df = temp_df[temp_df['Niederschlag_in_Liter_pro_m²'] >= 0]
    
    df_list.append(temp_df)

# Concatenate all DataFrames into one
df_final = pd.concat(df_list, ignore_index=True)

# Display first few rows to check
print(df_final.head())

# Get min and max year from df_final
min_year = df_final['Jahr'].min()
max_year = df_final['Jahr'].max()

# Count how many times rainfall was greater than RainyDayCutoff per weekday
df_rainy_days = df_final[df_final['Niederschlag_in_Liter_pro_m²'] > RainyDayCutoff].groupby('Wochentag', as_index=False).size()

# Define the correct weekday order
weekday_order = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

# Convert Wochentag to categorical type with defined order and sort
df_rainy_days['Wochentag'] = pd.Categorical(df_rainy_days['Wochentag'], categories=weekday_order, ordered=True)
df_rainy_days = df_rainy_days.sort_values('Wochentag')

# Plot the data
plt.style.use('dark_background')
plt.figure(figsize=(8, 6))
plt.bar(df_rainy_days['Wochentag'], df_rainy_days['size'], color='deepskyblue', edgecolor='black', linewidth=0.8)
plt.xlabel('Wochentag')
plt.grid(visible=True, color='gray', linestyle='--', linewidth=1, alpha=0.5)
plt.ylabel(f'Anzahl der Regentage (>{RainyDayCutoff} Liter/m²)')
plt.title(f'Anzahl der Regentage pro Wochentag ({min_year}–{max_year})')
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