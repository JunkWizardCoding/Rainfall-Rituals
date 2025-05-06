# 🌧️ Rainfall Rituals: Munich Rain Analysis 📊🔮

Welcome to **Rainfall Rituals**, a meteorological spellbook of Python scripts that analyze over 40 years of rainfall data from Munich. I originally started this project to find out **weather** there's more rain on weekends versus weekdays. Turns out that yes, there is a slight effect, but more interestingly, wednesdays are consistently the dryest!

Each script has both **English** and **German** versions for accessibility and linguistic clarity.

---

## 🧪 What’s Inside?

This repository contains six Python scripts and supporting material:

### 📁 Scripts

| Script Name                          | Description |
|-------------------------------------|-------------|
| `AverageRainfallWeekdayScriptEn.py` | Calculates average rainfall per weekday |
| `StrongRainfallWeekdayScriptEn.py`  | Counts days with rainfall above a defined threshold per weekday |
| `YearlyHeavyRainfallScriptEn.py`    | Plots yearly total rainfall, colored by frequency of heavy rain days |
| `*Ge.py` equivalents                | German versions of the above scripts |

### 📁 Sample Data

Three folders of `.csv` files  with daily rainfall records from three different Munich weather stations. Each file contains:

- `Datum`: Date in format `Mo 01.01.` (includes weekday prefix)
- `Niederschlag_in_Liter_pro_m²`: Daily rainfall in L/m²

Weather data provided by the Deutsche Wetterdienst, sourced through [wetterkontor.de](https://www.wetterkontor.de/de/wetter/deutschland/rueckblick.asp?id=175&datum0=01.01.2020&datum1=31.03.2020&jr=2025&mo=3&datum=18.03.2025&t=8&part=0)


### 📁 Sample Graphs

Rendered `.png` visualizations produced by the scripts. Includes average and heavy rainfall patterns per weekday and per year.


---

## 🧙‍♂️ Usage Instructions

### 1. Setup

Make sure you have Python 3.7 installed, then install the required packages:

```bash
pip install pandas matplotlib

### 2. Folder Structure

Your project directory should look like this:

```
Rainfall-Rituals/
├── data/
│   ├── Muenchen-Stadt/
│   │	├── Muenchen_Stadt_1982T3.csv
│   │	└── ...
│   ├── Muenchen-Flughafen/
│   └── ...
├── graphs/
│   ├── average_weekday_rainfall.png
│   ├── heavy_rain_days_per_weekday.png
│   └── yearly_total_rainfall.png
├── AverageRainfallWeekdayScriptEn.py
├── AverageRainfallWeekdayScriptGe.py
├── StrongRainfallWeekdayScriptEn.py
├── StrongRainfallWeekdayScriptGe.py
├── YearlyHeavyRainfallScriptEn.py
├── YearlyHeavyRainfallScriptGe.py
└── README.md
```

Update the file paths in each script to match your system, e.g.:

```python
for filename in glob.glob("data/Muenchen-Flughafen/*.csv"):
```

### 3. How to Run

Choose your preferred language and script. Then run with Python:

```bash
python AverageRainfallWeekdayScriptEn.py
```

Each script performs the following:

- Loads `.csv` data files from the `data/` directory
- Extracts "year" from the file name
- Extracts and parses dates and rainfall values
- Filters invalid or erroneous data
- Performs statistical grouping by weekday or year
- Generates a plot and displays it
- Saves output plots into the `graphs/` folder


### 4. Customization

- **Rain threshold** in the strong rainfall scripts can be adjusted via the `RainyDayCutoff` variable.
- Change the data path by editing the `glob.glob("...")` line near the top of each script.
- Modify figure aesthetics via `matplotlib` settings near the bottom.
- Modify the data frame by adding logic before the data concatenation into df_final, for example to find out how often it rains on your birthday!

### 5. Requirements

- Python 3.7+
- Required packages:
  ```bash
  pip install pandas matplotlib
  ```

### 6. License & Credits

Crafted with care by [Merlin](https://github.com/JunkWizardCoding), master of natural magic and data rituals.  
Released under the MIT License. Enjoy playing with my work!

---