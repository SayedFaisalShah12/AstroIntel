import streamlit as st
from api.nasa_client import NASAClient
from visualization.charts import plot_neo_scatter
import datetime

def app():
    st.header("Asteroid Watch ☄️")
    st.write("Monitoring Near Earth Objects (NEOs) - closest approach today.")

    client = NASAClient()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.date.today())
    with col2:
        end_date = st.date_input("End Date", datetime.date.today())
    
    if st.button("Scan Sky"):
        with st.spinner("Scanning for asteroids..."):
            # Convert to string
            s_str = start_date.strftime("%Y-%m-%d")
            e_str = end_date.strftime("%Y-%m-%d")
            
            data = client.get_neo_feed(s_str, e_str)
            
            if data and "near_earth_objects" in data:
                # Flatten data for visualization
                neo_list = []
                count = data.get("element_count", 0)
                st.metric("Asteroids Detected", count)
                
                for date_key in data["near_earth_objects"]:
                    for obj in data["near_earth_objects"][date_key]:
                        # Extract relevant fields
                        name = obj["name"]
                        diameter = obj["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
                        is_hazardous = obj["is_potentially_hazardous_asteroid"]
                        
                        # Close approach data (take the first one usually)
                        if obj["close_approach_data"]:
                            cad = obj["close_approach_data"][0]
                            miss_dist = float(cad["miss_distance"]["kilometers"])
                            velocity = float(cad["relative_velocity"]["kilometers_per_hour"])
                            
                            neo_list.append({
                                "name": name,
                                "diameter_min_km": diameter,
                                "hazardous": is_hazardous,
                                "miss_distance_km": miss_dist,
                                "velocity_kph": velocity,
                                "close_approach_date": cad["close_approach_date_full"]
                            })
                
                # Visualize
                if neo_list:
                    st.plotly_chart(plot_neo_scatter(neo_list), use_column_width=True)
                    
                    st.subheader("Hazardous Asteroids Detected")
                    hazardous = [n for n in neo_list if n["hazardous"]]
                    if hazardous:
                        st.dataframe(hazardous)
                    else:
                        st.success("No hazardous asteroids in this range!")
                else:
                    st.warning("No approach data found.")
            else:
                st.error("Failed to fetch NEO data.")
