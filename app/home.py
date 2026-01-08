import streamlit as st
import pandas as pd
from api.nasa_client import NASAClient

def app():
    st.title("Welcome to AstroIntel 🌌")
    st.markdown("### Artificial Intelligence for Space Analytics")
    
    client = NASAClient()
    
    # APOD Section
    st.subheader("Astronomy Picture of the Day")
    apod_data = client.get_apod()
    
    if apod_data:
        if apod_data.get("media_type") == "image":
            st.image(apod_data.get("url"), caption=apod_data.get("title"), use_column_width=True)
        elif apod_data.get("media_type") == "video":
            st.video(apod_data.get("url"))
            
        with st.expander("Read Explanation"):
            st.write(apod_data.get("explanation"))
            st.caption(f"Date: {apod_data.get('date')}")
    else:
        st.error("Could not fetch APOD data. The NASA API might be timing out.")
        if st.button("Retry Load APOD"):
            st.rerun()

    st.markdown("---")
    st.info("👈 Use the sidebar to navigate between modules.")
