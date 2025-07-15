import pandas as pd
from datetime import datetime

def extract_month(df):
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    return df

def encode_categorical(df, cols):
    for col in cols:
        df[col] = pd.Categorical(df[col]).codes
    return df

def extract_package_volume(df):
    df['Package_L'] = pd.to_numeric(
        df['Package'].str.extract(r'([\d.]+)')[0], errors='coerce'
    ) * 35.239
    return df