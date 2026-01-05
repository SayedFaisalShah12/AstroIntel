import joblib
import pandas as pd
import os

class MarsPredictor:
    def __init__(self, model_path='models/mars_temp_model.pkl'):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = None

    def predict(self, ls, pressure, wind_speed):
        if not self.model:
            return None
        
        input_data = pd.DataFrame({
            'ls': [ls],
            'pressure': [pressure],
            'wind_speed': [wind_speed]
        })
        
        return self.model.predict(input_data)[0]
