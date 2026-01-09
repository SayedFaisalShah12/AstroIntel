# AstroIntel 🚀🌌
### AI-Powered Space Analytics & Exploration Platform

**AstroIntel** is a comprehensive space analytics dashboard built with Python and Streamlit. It leverages NASA's public APIs to provide real-time data on Near-Earth Objects (NEOs), Mars rover imagery, detailed Earth observation, and an AI-powered weather prediction model for the Martian surface.   

### Links:
https://sayedfaisalshah12-astrointel-dashboard-okvafp.streamlit.app/

---

## ✨ Key Features

### 1. 🏠 **Home Dashboard & APOD**
- Daily **Astronomy Picture of the Day (APOD)** fetching.
- Detailed explanations and high-quality media (images/videos) straight from NASA.

### 2. ☄️ **Asteroid Watch (NEO Monitoring)**
- Track **Near-Earth Objects** approaching Earth today.
- Interactive **Plotly visualizations** showing asteroid size vs. miss distance.
- Alert system for **Potentially Hazardous Asteroids (PHAs)**.

### 3. 🌍 **Earth Views (EPIC)**
- Access daily imagery from the **Deep Space Climate Observatory (DSCOV)** satellite.
- View the "Blue Marble" rotating Earth images with date-specific filtering.

### 4. 🔴 **Mars Exploration Hub**
- **Rover Photos**: Browse raw images from the **Curiosity Rover** by Sol (Martian day) and Camera type (FHAZ, RHAZ, MAST, etc.).
- **AI Weather Predictor**: A Machine Learning module that predicts **Mars Surface Temperature** based on atmospheric pressure, wind speed, and seasonal solar longitude.

### 5. 🖼️ **NASA Image Gallery**
- comprehensive search interface for the entire **NASA Image and Video Library**.
- View high-resolution astronomical images with detailed metadata.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (for rapid interactive web/data app development)
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (Random Forest Regressor)
- **Visualization**: Plotly Interactive Charts
- **API Connectivity**: Python `requests` library
- **APIs Used**:
  - NASA APOD API
  - NASA NeoWs (Near Earth Object Web Service)
  - NASA EPIC API
  - NASA Mars Rover Photos API
  - NASA Image and Video Library

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher installed.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AstroIntel.git
cd AstroIntel
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
You need a NASA API Key to access the data.
1. Sign up for a free key at [api.nasa.gov](https://api.nasa.gov/).
2. Create a `.env` file in the root directory:
```bash
touch .env
```
3. Add your key to the file:
```env
NASA_API_KEY=your_actual_api_key_here
```

### 5. Run the Application
```bash
streamlit run dashboard.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
AstroIntel/
├── api/
│   └── nasa_client.py    # Handles all HTTP requests to NASA endpoints
├── app/
│   ├── home.py           # Landing page & APOD
│   ├── asteroids.py      # NEO tracking logic
│   ├── earth.py          # EPIC imagery logic
│   ├── mars.py           # Rover photos & ML prediction interface
│   └── gallery.py        # Image library search
├── data/
│   └── mars_weather_synthetic.csv # Data for model training/visualization
├── ml/
│   ├── predictor.py      # ML Model definition and inference logic
│   └── generate_data.py  # Script to generate synthetic training data
├── models/
│   └── mars_temp_model.pkl # Serialized trained ML model
├── visualization/
│   └── charts.py         # Plotly plotting functions
├── dashboard.py          # Main entry point (Streamlit App)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🧠 Machine Learning Model
The Mars Weather Predictor uses a **Random Forest Regressor** to estimate surface temperatures. 
- **Inputs**: Solar Longitude ($L_s$), Atmospheric Pressure (Pa), Wind Speed (m/s).
- **Output**: Surface Temperature (°C).
- You can retrain the model or generate new data using scripts in the `ml/` folder.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is open-source and available under the MIT License.
