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

print("Shape (rows, columns)", df.shape)
print("\n\nColumn names:\n", df.columns.tolist())
print("\n\nFirst 5 rows:\n", df.head())
print("\n\nData types:\n", df.dtypes)
print("\n\nMissing values per column:\n", df.isnull().sum())