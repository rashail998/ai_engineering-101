import zipfile
import os
import pandas as pd

zip_filename = 'sales_data.zip'
extract_to = 'data_folder'

# 1. Automate Unzipping
with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall(extract_to)
    print(f"Extracted {zip_filename} to {extract_to}/")


# 2. Load the data (Update 'movies.csv' to the name of the name of the file inside the zip)
# You can check the file name by opening the zip manually or using zip_ref.namelist()
csv_file = os.path.join(extract_to, 'Sales-Export_2019-2020.csv')
df = pd.read_csv(csv_file)


# 3. Stripping white spaces from column names
df.columns = df.columns.str.strip()

# 4. Covnerting order_vlaue_EUR from text to real number only for this dataset in particular
df['order_value_EUR'] = df['order_value_EUR'].str.replace(',', '').astype(float)

# 5. Converting date column to actual datetime type
df['date'] = pd.to_datetime(df['date'])


# Sanity check
print("\nCleaned columns:\n", df.columns.tolist())
print("\nData type after cleaning:\n", df.dtypes)
print("\nFirst 5 rows:\n", df.head())


# Saving the cleaned version so we don't repeat this every time
df.to_csv('sales_data_cleaned.csv', index=False)
print("\nSaved cleaned data file as 'sales_data_cleaned.csv'")