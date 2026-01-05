import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def train():
    data_path = 'data/mars_weather_synthetic.csv'
    if not os.path.exists(data_path):
        print("Data file not found. Please run generate_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Features: Solar Longitude, Pressure, Wind Speed
    X = df[['ls', 'pressure', 'wind_speed']]
    # Target: Avg Temperature
    y = df['avg_temp']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print(f"Model Trained. RMSE: {rmse:.2f}, R2: {r2:.2f}")
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/mars_temp_model.pkl')
    print("Model saved to models/mars_temp_model.pkl")

if __name__ == "__main__":
    train()
