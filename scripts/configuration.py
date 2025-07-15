import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH       = os.path.join(BASE_DIR, "data", "US-pumpkins.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
REPORT_PATH         = os.path.join(BASE_DIR, "output", "analysis_report.json")
FIGURES_DIR         = os.path.join(BASE_DIR, "output", "figures")