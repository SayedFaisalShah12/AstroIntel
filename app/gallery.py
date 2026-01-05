import streamlit as st
from api.nasa_client import NASAClient

def app():
    st.header("NASA Image Gallery 🖼️")
    
    query = st.text_input("Search NASA's Library", "Black Hole")
    
    if st.button("Search"):
        client = NASAClient()
        with st.spinner("Searching..."):
            results = client.search_images(query)
            
            if results and "collection" in results:
                items = results["collection"]["items"]
                st.success(f"Found {len(items)} results.")
                
                for item in items[:20]: # Limit to 20
                    data = item["data"][0]
                    links = item.get("links", [])
                    
                    if links:
                        img_url = links[0]["href"]
                        title = data.get("title", "No Title")
                        desc = data.get("description", "No description.")
                        
                        st.subheader(title)
                        st.image(img_url, use_container_width=True)
                        with st.expander("Description"):
                            st.write(desc)
                        st.divider()
            else:
                st.error("Search failed.")
