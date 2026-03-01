"""
input module reads gdp data from different file formats
"""
import json
import re
import pandas as pd
from typing import List, Dict, Any


class JSONReader:
    """reads gdp data from json file"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        print(f"json reader ready {filepath}")
    
    def read(self):
        print(f"\nreading json file")
        try:
            with open(self.filepath, 'r') as f:
                content = f.read()
            content = re.sub(r':\s*NaN\b', ': null', content)
            content = re.sub(r':\s*#[^,\n\}]*', ': null', content)
            data = json.loads(content)
            print(f"loaded {len(data)} countries from json")
            df = pd.DataFrame(data)
            print("reshaping data wide to long")
            year_columns = [col for col in df.columns if str(col).isdigit()]
            id_columns = ['Country Name', 'Country Code', 'Continent']
            df_long = pd.melt(df, id_vars=[col for col in id_columns if col in df.columns], value_vars=year_columns, var_name='Year', value_name='Value')
            print("cleaning data")
            df_long = df_long.dropna(subset=['Value'])
            df_long['Year'] = df_long['Year'].astype(int)
            df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
            df_long = df_long.dropna()
            if 'Continent' in df_long.columns:
                df_long = df_long.rename(columns={'Continent': 'Region'})
            print(f"data ready {len(df_long)} rows")
            return df_long.to_dict('records')
        except FileNotFoundError:
            print(f"error file not found {self.filepath}")
            return []
        except Exception as e:
            print(f"error {e}")
            return []


class CSVReader:
    """reads gdp data from csv file"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        print(f"csv reader ready {filepath}")

    def read(self):
        print(f"\nreading csv file")
        try:
            df = pd.read_csv(self.filepath)
            print(f"loaded {len(df)} records")
            if 'Year' in df.columns and 'Value' in df.columns:
                print("data already in long format")
                df = df.dropna(subset=['Value'])
                df['Year'] = df['Year'].astype(int)
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                df = df.dropna()
            else:
                year_columns = [col for col in df.columns if str(col).isdigit()]
                id_columns = ['Country Name', 'Country Code', 'Continent']
                df = pd.melt(df, id_vars=[col for col in id_columns if col in df.columns], value_vars=year_columns, var_name='Year', value_name='Value')
                df = df.dropna(subset=['Value'])
                df['Year'] = df['Year'].astype(int)
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                df = df.dropna()
            if 'Continent' in df.columns:
                df = df.rename(columns={'Continent': 'Region'})
            print(f"data ready {len(df)} rows")
            return df.to_dict('records')
        except Exception as e:
            print(f"error {e}")
            return []


class ExcelReader:
    """reads gdp data from excel file"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        print(f"excel reader ready {filepath}")

    def read(self):
        print(f"\nreading excel file")
        try:
            df = pd.read_excel(self.filepath)
            print(f"loaded {len(df)} records")
            year_columns = [col for col in df.columns if str(col).isdigit()]
            id_columns = ['Country Name', 'Country Code', 'Continent']
            df_long = pd.melt(df, id_vars=[col for col in id_columns if col in df.columns], value_vars=year_columns, var_name='Year', value_name='Value')
            df_long = df_long.dropna(subset=['Value'])
            df_long['Year'] = df_long['Year'].astype(int)
            df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
            df_long = df_long.dropna()
            if 'Continent' in df_long.columns:
                df_long = df_long.rename(columns={'Continent': 'Region'})
            print(f"data ready {len(df_long)} rows")
            return df_long.to_dict('records')
        except Exception as e:
            print(f"error {e}")
            return []


