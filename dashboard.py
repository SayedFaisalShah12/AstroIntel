import streamlit as st
import app.home
import app.asteroids
import app.earth
import app.mars
import app.gallery

# Page Config
st.set_page_config(
    page_title="AstroIntel",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle, #0b0d17 0%, #161b33 100%);
        color: #e0e0e0;
    }
    .stSidebar {
        background-color: #0b0d17;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #61dafb;
    }
    .stButton>button {
        background-color: #61dafb;
        color: #0b0d17;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #4fa8d1;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []
    
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
        
    def run(self):
        with st.sidebar:
            st.title("AstroIntel 🚀")
            st.markdown("---")
            app = st.radio(
                "Navigation",
                self.apps,
                format_func=lambda app: app['title']
            )
            st.markdown("---")
            st.info("Developed by AstroIntel AI")
            
        app['function']()

def main():
    multi_app = MultiApp()
    
    multi_app.add_app("Home", app.home.app)
    multi_app.add_app("Asteroid Watch", app.asteroids.app)
    multi_app.add_app("Earth Views", app.earth.app)
    multi_app.add_app("Mars Exploration", app.mars.app)
    multi_app.add_app("Image Gallery", app.gallery.app)
    
    multi_app.run()

if __name__ == "__main__":
    main()
