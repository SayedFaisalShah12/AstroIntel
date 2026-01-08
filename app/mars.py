import streamlit as st
from api.nasa_client import NASAClient
from ml.predictor import MarsPredictor
from visualization.charts import plot_temp_predictions
import pandas as pd
import os

def app():
    st.header("Mars Exploration 🔴")
    
    tab1, tab2 = st.tabs(["Rover Photos", "Weather Prediction (AI)"])
    
    client = NASAClient()

    with tab1:
        st.subheader("Curiosity Rover Photos")
        sol = st.slider("Sol (Martian Day)", 1, 3000, 1000)
        cam = st.selectbox("Camera", ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"])
        
        if st.button("Get Photos"):
            photos_data = client.get_mars_rover_photos(sol=sol, rover="curiosity")
            if photos_data and "photos" in photos_data:
                photos = photos_data["photos"]
                # Filter by camera
                filtered_photos = [p for p in photos if p["camera"]["name"] == cam]
                
                if filtered_photos:
                    st.success(f"Found {len(filtered_photos)} photos.")
                    # Show first 5
                    cols = st.columns(3)
                    for idx, photo in enumerate(filtered_photos[:9]):
                        with cols[idx % 3]:
                            st.image(photo['img_src'], caption=f"{photo['rover']['name']} - {photo['camera']['full_name']}", use_column_width=True)
                else:
                    st.warning(f"No photos found for {cam} on Sol {sol}.")
            else:
                st.error("Failed to fetch rover data.")

    with tab2:
        st.subheader("Mars Weather Prediction (ML)")
        st.write("Predict Mars Surface Temperature based on atmospheric conditions.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            ls_input = st.slider("Solar Longitude (Season)", 0, 360, 90)
        with col2:
            press_input = st.slider("Pressure (Pa)", 600, 1200, 800)
        with col3:
            wind_input = st.slider("Wind Speed (m/s)", 0.0, 20.0, 5.0)
            
        if st.button("Predict Temperature"):
            predictor = MarsPredictor()
            if predictor.model:
                pred_temp = predictor.predict(ls_input, press_input, wind_input)
                st.metric("Predicted Temperature", f"{pred_temp:.2f} °C")
                
                # Show context on historical chart
                # Load history
                if os.path.exists('data/mars_weather_synthetic.csv'):
                    hist_df = pd.read_csv('data/mars_weather_synthetic.csv')
                    fig = plot_temp_predictions(hist_df, pred_temp)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Model not found. Please ensure training is complete.")
