import pandas as pd
from datetime import datetime

def load_data(path):
    return pd.read_csv(path)

def summarize_data(df):
    return {
        "total_records": len(df),
        "start_date": str(df['Date'].min()) if 'Date' in df.columns else "N/A",
        "end_date": str(df['Date'].max()) if 'Date' in df.columns else "N/A",
        "unique_cities": df['City'].nunique() if 'City' in df.columns else "N/A",
        "unique_types": df['Type'].nunique() if 'Type' in df.columns else "N/A"
    }

def price_statistics(df):
    return {
        "low_price_mean": df['Low Price'].mean() if 'Low Price' in df.columns else "N/A",
        "high_price_mean": df['High Price'].mean() if 'High Price' in df.columns else "N/A",
        "avg_price_mean": df['Avg Price'].mean() if 'Avg Price' in df.columns else "N/A",
        "avg_price_std": df['Avg Price'].std() if 'Avg Price' in df.columns else "N/A",
        "avg_price_min": df['Avg Price'].min() if 'Avg Price' in df.columns else "N/A",
        "avg_price_max": df['Avg Price'].max() if 'Avg Price' in df.columns else "N/A"
    }

def monthly_price_trend(df):
    if 'Date' not in df.columns or 'Avg Price' not in df.columns:
        return "缺少日期或价格列"
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_avg = df.set_index('Date').resample('M')['Avg Price'].mean()
    return {
        "months": monthly_avg.index.strftime('%Y-%m').tolist(),
        "prices": monthly_avg.values.tolist()
    }

def price_correlation(df):
    cols = ['Low Price', 'High Price', 'Avg Price']
    if set(cols).issubset(df.columns):
        return df[cols].corr().to_dict()
    return "缺少价格列"