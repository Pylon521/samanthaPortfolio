# %%
"""
Initial Setup for Pew Research Center Global Attitudes Spring 2024 Survey Analysis
- extract data from zip file, and load CSV data into pandas dataframe
"""
import zipfile
import os
import pandas as pd

zip_path = os.getcwd() + '\\Data\\'+ 'Pew-Research-Center-Global-Attitudes-Spring-2024-Survey-Public.zip'
extract_path = "Data"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

os.listdir(extract_path)

# %%
"""
investigate response data, check and remove missing data, and save a base csv file for analysis
"""
csv = os.getcwd() + '\\Data\\' + 'Pew Research Center Global Attitudes Spring 2024 Dataset CSV.csv'
df_csv = pd.read_csv(csv)
print(df_csv.dtypes)

missing = df_csv.isna() | (df_csv == " ")
missing = missing.sum()
missing = missing.to_frame(name='missing_count')
print(type(missing))
missing['total_row'] = df_csv.shape[0]
missing['missing_pct'] = missing['missing_count']/missing['total_row']
# missing.sort_values(by='missing_pct', ascending=False, inplace=True)
print('number of columns without missing data:', len(missing[missing['missing_pct']== 0]))
print('percent of columns with missing data:', len(missing[missing['missing_pct']!= 0])/len(missing))
missing
# 41 columns are the starting point of the analysis
# if data is not sufficient, will expand using other columns with minimal missing data

# %%
col_used = missing[missing['missing_pct']== 0].index
print(list(col_used))
df_cleaned = df_csv[col_used]
df_cleaned.to_csv('base.csv', index=False)
df_cleaned.info()

# %%
"""
correlation analysis on cleaned data, provide a focus point for future analysis
"""
corr = df_cleaned.corr()
corr.to_excel('corr.xlsx')
corr


# %%

"""
review short form questions to original questions
"""
# excel = os.getcwd() + '\\Data\\' + 'Pew Research Center Global Attitudes Spring 2024 Data Dictionary.xlsx'
# df_excel = pd.read_excel(excel)
# df_excel

"""
mapping category values to labels
"""
import xml.etree.ElementTree as ET

# load XML
xml = os.getcwd() + '\\Data\\' + 'Pew Research Center Global Attitudes Spring 2024 Metadata.xml'
tree = ET.parse(xml)
root = tree.getroot()

# namespace mapping from your XML header
ns = {"ddi": "ddi:codebook:2_5"}

rows = []

# loop through each variable
for var in root.findall(".//ddi:var", ns):
    var_id = var.get("ID")
    var_name = var.get("name")
    var_label = var.findtext("ddi:labl", namespaces=ns)
    
    # loop through categories
    for cat in var.findall("ddi:catgry", ns):
        cat_value = cat.findtext("ddi:catValu", namespaces=ns)
        cat_label = cat.findtext("ddi:labl", namespaces=ns)
        rows.append({
            "var_id": var_id,
            "var_name": var_name,
            "var_label": var_label,
            "cat_value": cat_value,
            "cat_label": cat_label
        })

# convert to dataframe
df = pd.DataFrame(rows)

# save to CSV
df.to_csv("variables_flat.csv", index=False)