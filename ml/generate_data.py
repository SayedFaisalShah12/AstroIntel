import pandas as pd
import numpy as np
import random

def generate_mars_data():
    # Simulate a Martian year (668 sols)
    sols = np.arange(1, 669)
    # Seasonal effect on temperature (sinusoidal)
    # Avg temp -60C, fluctuation +/- 20C
    min_temp = -60 + 20 * np.sin(2 * np.pi * sols / 668) + np.random.normal(0, 2, 668)
    max_temp = -10 + 20 * np.sin(2 * np.pi * sols / 668) + np.random.normal(0, 2, 668)
    avg_temp = (min_temp + max_temp) / 2
    
    # Pressure (Pascals) - usually higher in winter
    pressure = 800 + 50 * np.cos(2 * np.pi * sols / 668) + np.random.normal(0, 5, 668)
    
    # Wind Speed (m/s)
    wind_speed = np.random.lognormal(mean=1.5, sigma=0.5, size=668)
    
    # Solar Longitude (0-360) loosely follows sols
    ls = (sols / 668 * 360) % 360
    
    df = pd.DataFrame({
        'sol': sols,
        'ls': ls, # Solar Longitude
        'pressure': pressure,
        'wind_speed': wind_speed,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'avg_temp': avg_temp
    })
    
    return df

if __name__ == "__main__":
    df = generate_mars_data()
    import os
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/mars_weather_synthetic.csv', index=False)
    print("Synthetic Mars weather data generated and saved to data/mars_weather_synthetic.csv")
