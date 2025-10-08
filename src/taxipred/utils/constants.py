from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Models
MODEL_FILE = 'rf_r2_088.joblib'
SCALER_FILE = 'minmax_scaler.joblib'

MODEL_PATH = BASE_DIR / "models" / MODEL_FILE
SCALER_PATH = BASE_DIR / "models" / SCALER_FILE

# Data
ORIGINAL_DATA_FILE = BASE_DIR / "data" / "taxi_trip_pricing.csv"
PREDICTION_DATA_FILE = BASE_DIR / "data" / "predictions_lr_knn.csv"

# DATA_PATH = Path(__file__).parents[1] / "data"