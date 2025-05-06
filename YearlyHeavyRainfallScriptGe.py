# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 22:06:19 2025

@author: Merli <|:3
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

# Read data, extract weekday, full date, and year from filename
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

# Get min and max year from df_final
min_year = df_final['Jahr'].min()
max_year = df_final['Jahr'].max()

# Display first few rows to check
print(df_final.head())

# Count total rainfall per year
df_rainfall_per_year = df_final.groupby('Jahr', as_index=False)['Niederschlag_in_Liter_pro_m²'].sum()

# Count number of heavy rainfall days per year
df_heavy_rain_days = df_final[df_final['Niederschlag_in_Liter_pro_m²'] > RainyDayCutoff].groupby('Jahr', as_index=False).size()

# Merge heavy rainfall count into main DataFrame
df_rainfall_per_year = df_rainfall_per_year.merge(df_heavy_rain_days, on='Jahr', how='left').fillna(0)

# Normalize rainy days count for color mapping (0 → light blue, max → dark blue)
min_rain_days = df_rainfall_per_year['size'].min()
max_rain_days = df_rainfall_per_year['size'].max()
df_rainfall_per_year['color_intensity'] = (df_rainfall_per_year['size'] - min_rain_days) / (max_rain_days - min_rain_days)

# Define colormap from light blue to dark blue
colors = plt.cm.Blues(df_rainfall_per_year['color_intensity'])

# Plot rainfall per year with dynamic color
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(
    df_rainfall_per_year['Jahr'],
    df_rainfall_per_year['Niederschlag_in_Liter_pro_m²'],
    color=colors,
        )
ax.set_xlabel('Jahr')
ax.set_ylabel('Gesamtniederschlag (Liter/m²)')
ax.set_title(f'Jährlicher Gesamtniederschlag\nFarbskala nach Regentagen > {RainyDayCutoff} Liter/qm')
plt.grid(visible=True, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Add color bar on the right side
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=min_rain_days, vmax=max_rain_days))
sm.set_array([])  # Needed for matplotlib to properly show scalar mappable in colorbar
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Anzahl der starken Regentage')
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