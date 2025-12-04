# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 21:09:55 2025

@author: haley

Python Code to Download the Full SOHO / LASCO CDAW CME Catalog

"""

import pandas as pd
import requests
# from bs4 import BeautifulSoup
from datetime import datetime
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def download_cdaw_catalog():
    """
    Downloads the full SOHO/LASCO CDAW CME catalog (1996–present)
    and returns a Pandas DataFrame with all CME events.
    
    Data source:
    https://cdaw.gsfc.nasa.gov/CME_list/
    """
    # https://cdaw.gsfc.nasa.gov/CME_list/
    # base_url = "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL/"
    base_url = r"https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL_ver2/"
    
    # Start year of LASCO CME catalog
    start_year = 1996
    end_year = datetime.now().year

    all_cmes = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            #url = f"{base_url}{year}_{month:02d}/"
            url = f"{base_url}{year}_{month:02d}/univ{year}_{month:02d}.html"
            
            try:
                print(f"Fetching {url} ...")
                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    continue  # Skip missing months

                # Parse HTML and find data tables
                tables = pd.read_html(response.text)
                if len(tables) == 0:
                    continue

                # CDAW monthly pages normally have one main table
                df = tables[0]
                
                # Add metadata
                df["Year"] = year
                df["Month"] = month

                all_cmes.append(df)

            except Exception as e:
                print(f"Error fetching {url}: {e}")
                continue

    # Combine all monthly tables
    if len(all_cmes) == 0:
        raise RuntimeError("No CME data could be downloaded.")

    full_catalog = pd.concat(all_cmes, ignore_index=True)

    # Export
    f=os.path.join("Data", "CDAW_CME_Catalog.csv")

    # Save locally
    full_catalog.to_csv(f, index=False)
    print("Saved full CME catalog with", len(full_catalog), "entries.")


def load_cdaw_catalog():
    f=os.path.join("Data", "CDAW_CME_Catalog.csv")
    df = pd.read_csv(f)
    # df.drop(['Unnamed: 0', 'Description'], axis=1, inplace=True)
    return df

def load_cdaw_catalog_processed():
    f=os.path.join("Data", "CDAW_CME_Catalog_Processed.csv")
    df = pd.read_csv(f)
    return df

def get_decimal_day(row):
    date = row['First C2 Appearance Date Time [UT]']
    day = float(date.split("/")[2])
    time = row['First C2 Appearance Date Time [UT].1']
    hour, minute, second = time.split(":")
    
    # Get decimals.
    min_dec = float(minute)+float(second)/60
    hr_dec = float(hour)+min_dec/60
    day_dec = day+hr_dec/24
    
    return day_dec

def get_date(row):
    date = row['First C2 Appearance Date Time [UT]']
    day = float(date.split("/")[2])
    time = row['First C2 Appearance Date Time [UT].1']
    hour, minute, second = time.split(":")    
    return [int(day), int(hour), int(minute), int(second)]

def process_cdaw_data(df):
    # Convert common remarks to new features.
    for substring in ['Poor Event', 'Very Poor Event', 'Partial Halo', \
                      'Only C2', 'Only C3', 'modified']:
        new_col = df['Remarks'].str.contains(substring, case=False, na=False).astype(int)
        
        # Check if there are enough values to matter.
        if sum(new_col) > len(df)/10 and sum(new_col) < len(df)*9/10:
            # Save as new feature.
            df[substring] = new_col
            
    # Combine remarks on measurement difficulties.
    remarks_meas = ['Unable to measure', 'Uncertain width', 'Difficult to measure width']
    for substring in remarks_meas:
        df[substring] = df['Remarks'].str.contains(substring, case=False, na=False).astype(int)
    df['Measurement Difficulties'] = 0
    df.loc[(df[remarks_meas[0]] == 1) | (df[remarks_meas[1]] == 1) |  (df[remarks_meas[2]] == 1), 'Measurement Difficulties'] = 1
    df.drop(remarks_meas, axis=1, inplace=True)
    
    df.drop(['Remarks', 'Movies, plots, & links'], axis=1, inplace=True)
    
    
    for col in df:
        if isinstance(df[col].iloc[0], str):
            df[col] = df[col].apply(lambda x: x if "---" not in x else np.nan)
    
    # Get date and time.
    #df['Decimal Day'] = df.apply(get_decimal_day, axis=1)
    #df['Day, Hour, Minute, Second'] = df.apply(get_date, axis=1)
    
    df['Day'] = df.apply(lambda row: int(row['First C2 Appearance Date Time [UT]'].split("/")[2]), axis=1)
    df['Hour'] = df.apply(lambda row: int(row['First C2 Appearance Date Time [UT].1'].split(":")[0]), axis=1)
    df['Minute'] = df.apply(lambda row: int(row['First C2 Appearance Date Time [UT].1'].split(":")[1]), axis=1)
    df['Second'] = df.apply(lambda row: int(row['First C2 Appearance Date Time [UT].1'].split(":")[2]), axis=1)
    
    df.drop(['First C2 Appearance Date Time [UT].1', 'First C2 Appearance Date Time [UT]'], axis=1, inplace=True)
    
    # Fix any columns with non-numerical values.
    df["Angular Width [deg]"] = df["Angular Width [deg]"].apply(lambda x: float(x) if ">" not in x else float(x.replace(">", "")))
    
        
    # df["Linear Speed [km/s]"] = df["Linear Speed [km/s]"].apply(lambda x: x if "--" not in x else np.nan)
    # df["2nd-order Speed at final height [km/s]"] = df["2nd-order Speed at final height [km/s]"].apply(lambda x: x if "--" not in x else np.nan)
    
    if debug:
        # Check all columns in the DataFrame
        numeric_cols = df.dtypes.apply(pd.api.types.is_numeric_dtype)
        print(f"\nNumeric columns:\n{numeric_cols}")
    
    return df

def find_non_numeric_rows(df, col):
    # Function for debugging.
    
    # Convert the column to numeric, coercing errors to NaN
    coerced_column = pd.to_numeric(df[col], errors='coerce')

    # Create a boolean mask where True indicates a non-numeric value (NaN after coercion)
    non_numeric_mask = coerced_column.isnull()

    # Filter the DataFrame to show rows with non-numeric values in 'numeric_col'
    rows_with_non_numeric = df[non_numeric_mask]

    print(f"There were {len(rows_with_non_numeric)} non-numeric rows found:")
    print(rows_with_non_numeric[col])
    
def plot_missing_data(df):
    sns.heatmap(df.isna(), cmap='viridis')
    plt.show()
    
    for col in df:
        count = sum(df[col].isna())
        if count > 0:
            print(col, count, "NANs")
            
        # Decide whether to drop the feature or drop the rows with NANs.
        if count/len(df) > 0.1:
            # Drop feature if missing in more than 10% of rows.
            df.drop(col, axis=1, inplace=True)
        else:
            # Drop rows.
            drop_rows = df[df[col].isna()].index
            df.drop(drop_rows, axis=0, inplace=True)

    return df

def continuous_day_calendar(row):
    # Convert year, month, and day to the count of days since a set epoch.
    # Set epoch to midnight on Jan 1, 1996.
    epoch = datetime(1996, 1, 1, 0, 0, 0)
    year = row['Year']
    month = row['Month']
    day = row['Day']
    hour = row['Hour']
    minute = row['Minute']
    second = row['Second']
    date = datetime(year, month, day, hour, minute, second)
    
    # Get total seconds since epoch. Convert seconds to days.
    diff_seconds = (date - epoch).total_seconds()
    diff_days = diff_seconds/86400
    return diff_days
    
def clean_pa(x):
    if "Halo" in x:
        return np.nan
    else:
        return int(x)


# =============================================================================
# Process
# =============================================================================
debug = True

# =============================================================================
# Load and Pre-Process Data
# =============================================================================
# df0 = load_cdaw_catalog()
# df = process_cdaw_data(df0)
# df = plot_missing_data(df)
# f=os.path.join("Data", "CDAW_CME_Catalog_Processed.csv")

# df['Days Since Epoch'] = df.apply(continuous_day_calendar, axis=1)
# df.drop(['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second'], axis=1, inplace=True)
# df['Central PA [deg]'] = df['Central PA [deg]'].apply(clean_pa)
# # Drop acceleration column.
# # From CDAW database: "*1 Acceleration is uncertain due to either poor height measurement or a small number of height-time measurements (See Section 3.4 of Yashiro et al. 2004 for details)."
# df.drop('Accel [m/s2]', axis=1, inplace=True)

# df.to_csv(f, index=False)


# =============================================================================
# ML Model
# =============================================================================
df = load_cdaw_catalog_processed()


# for col in df.drop('Days Since Epoch', axis=1):
#     plt.figure()
#     plt.title(col)
#     plt.scatter(df['Days Since Epoch'], df[col], s=2)
#     plt.show()
    
    
# sns.scatterplot(df, x='Days Since Epoch', y='Central PA [deg]', hue='Measurement Difficulties')



# plt.figure(figsize=(10,6))
# sns.scatterplot(good_events, x='Days Since Epoch', y='Angular Width [deg]', hue='Measurement Difficulties')
# plt.show()
# plt.close()


# plt.figure(figsize=(10,6))
# sns.scatterplot(good_events[-100:], x='Days Since Epoch', y='Angular Width [deg]', hue='Measurement Difficulties')
# plt.show()
# plt.close()

# plt.figure(figsize=(10,6))
# sns.scatterplot(df, x='Days Since Epoch', y='Central PA [deg]', hue='Poor Event')
# plt.show()
# plt.close()

df['Mild Event'] = df['Poor Event'] | df['Very Poor Event'] | df['Only C2']
df.drop(['Poor Event', 'Very Poor Event', 'Only C2'], axis=1, inplace=True)
good_events = df.loc[(df['Mild Event']==0)].drop('Mild Event', axis=1)

boolean_cols = ['Mild Event', 'Measurement Difficulties']
value_cols = ['Central PA [deg]', 'Angular Width [deg]', 'Linear Speed [km/s]',
       '2nd-order Speed at final height [km/s]',
       '2nd-order Speed at 20 Rs [km/s]', 'MPA [deg]', 'Days Since Epoch']

# this_bool = boolean_cols[0]
# other_bool = boolean_cols[1]
# plt.figure(figsize=(6,6))
# sns.pairplot(df.drop(other_bool, axis=1), hue=this_bool, s=4)
# plt.savefig(os.path.join("Images", "CMEs_pairplot0.png"), dpi=300)
# plt.close()

# this_bool = boolean_cols[1]
# other_bool = boolean_cols[0]
# plt.figure(figsize=(8,8))
# sns.pairplot(df.drop(other_bool, axis=1), hue=this_bool)
# plt.savefig(os.path.join("Images", "CMEs_pairplot1.png"), dpi=300)
# plt.close()


# plt.figure(figsize=(6,6))
# sns.pairplot(good_events.drop("Measurement Difficulties", axis=1))
# plt.savefig(os.path.join("Images", "CMEs_pairplot2.png"), dpi=300)
# plt.close()


# plt.figure(figsize=(6,6))
# sns.scatterplot(good_events, x='Days Since Epoch', y='Central PA [deg]')
# plt.show()
# plt.close()


df['CPA Range'] = df['Central PA [deg]'].apply(lambda x: "180-360 deg" if x >180 else "0-180 deg")

# plt.figure(figsize=(10,6))
# sns.scatterplot(df, x='Days Since Epoch', y='Linear Speed [km/s]', hue='CPA Range')
# plt.show()
# plt.close()


# plt.figure(figsize=(10,10))
# sns.heatmap(good_events.corr(), cmap='jet')
# plt.tight_layout()
# plt.savefig(os.path.join("Images", "CMEs_corr.png"), dpi=300)
# plt.show()
# plt.close()



plt.figure(figsize=(10,6))
sns.scatterplot(df, x='Days Since Epoch', y='Linear Speed [km/s]', s=5)
plt.savefig(os.path.join("Images", "linear_speed.png"), dpi=300)
plt.close()

plt.figure(figsize=(10,6))
sns.scatterplot(df, x='Days Since Epoch', y='Angular Width [deg]', s=5)
plt.savefig(os.path.join("Images", "angular_width.png"), dpi=300)
plt.close()


def get_cme_ranking(row):
    # My custom CME ranking. 
    # 0 = no activity, 1 = minimal activity/poor event. 2 = full event 
    if row['Mild Event']:
        return 1
    else:
        return 2
df['CME Ranking'] = df.apply(get_cme_ranking, axis=1)

# For every pair of decimal values, you want to insert any integer values that 
# fall strictly between them, and the new rows should have 0 for all other columns.
def expand_with_integers(df, col):
    new_rows = []

    for i in range(len(df) - 1):
        current_val = df.loc[i, col]
        next_val = df.loc[i + 1, col]
        
        # Add current row
        new_rows.append(df.iloc[i])
        
        # Find integers between them
        start = int(np.ceil(current_val))
        end = int(np.floor(next_val))
        
        for v in range(start, end + 1):
            if current_val < v < next_val:
                # Create new row with v and zeros in other columns
                row = {c: 0 for c in df.columns}
                row[col] = v
                new_rows.append(pd.Series(row))
    
    # Add last row
    new_rows.append(df.iloc[-1])

    return pd.DataFrame(new_rows).reset_index(drop=True)

def fill_with_nominal_days(df, col):
    new_rows = []

    for i in range(len(df) - 1):
        current_val = df.loc[i, col]
        next_val = df.loc[i + 1, col]
        
        # Add current row
        new_rows.append(df.iloc[i])
        
        # Find out how many new rows we need to add.
        diff = next_val - current_val
        number_new_rows = np.floor(diff)
        step_size = diff/(number_new_rows+1)
        
        new_val = current_val
        for i in range(1, int(number_new_rows+1)):
            # Create new row with v and zeros in other columns
            new_val+=step_size
            row = {c: 0 for c in df.columns}
            row[col] = new_val
            new_rows.append(pd.Series(row))
 
    # Add last row
    new_rows.append(df.iloc[-1])
    return pd.DataFrame(new_rows).reset_index(drop=True)  
        

data = fill_with_nominal_days(df, 'Days Since Epoch')
# data = data[['Days Since Epoch', 'CME Ranking']]

# i =  42000
# plt.plot(data['Days Since Epoch'].iloc[i:], data['CME Ranking'].iloc[i:], lw=1)


data.to_excel(os.path.join("Data", "CDAW Nominal and Severe Database.xlsx"), index=False)