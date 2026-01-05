import streamlit as st
from api.nasa_client import NASAClient

def app():
    st.header("Earth Views (EPIC) 🌍")
    st.write("Earth Polychromatic Imaging Camera (DSCOV) - Daily Blue Marble.")

    client = NASAClient()
    
    # Date picker
    date = st.date_input("Select Date", None) # None implies latest
    
    if st.button("Load Images"):
        date_str = date.strftime("%Y-%m-%d") if date else None
        
        with st.spinner(f"Fetching images for {date_str or 'latest'}..."):
            images = client.get_epic_images(date_str)
            
            if images:
                st.success(f"Found {len(images)} images.")
                
                # Carousel or Grid
                # For EPIC, we need to construct the image URL
                # https://epic.gsfc.nasa.gov/archive/natural/2019/05/30/png/epic_1b_20190530011359.png
                
                for img in images:
                    # Construct URL
                    # Format of date in 'identifier' or 'date' field?
                    # API returns 'date': '2023-10-10 00:00:00'
                    img_date_str = img['date'].split(' ')[0]
                    year, month, day = img_date_str.split('-')
                    filename = img['image']
                    
                    # Url structure: https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{filename}.png
                    img_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{filename}.png"
                    
                    st.image(img_url, caption=f"{img['caption']} - {img['date']}", use_container_width=True)
                    st.divider()

            else:
                st.warning("No images found for this date. (EPIC data has a lag of 1-2 days usually).")
