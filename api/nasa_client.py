import os
import requests
import datetime
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

class NASAClient:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov"
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return self._get_mock_data(endpoint) # Fallback to mock data

    def _get_mock_data(self, endpoint):
        """Return mock data for demonstration purposes when API fails."""
        if endpoint == "/planetary/apod":
            return {
                "title": "Cosmic Pillars (Mock Data)",
                "date": datetime.date.today().strftime("%Y-%m-%d"),
                "explanation": "This is a placeholder image because the NASA API is currently unreachable. The Pillars of Creation are elephants trunks of interstellar gas and dust in the Eagle Nebula.",
                "media_type": "image",
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/68/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg"
            }
        elif "/mars-photos/api/v1/rovers" in endpoint:
             return {
                 "photos": [
                     {"id": 1, "img_src": "https://upload.wikimedia.org/wikipedia/commons/d/d8/NASA_Mars_Rover.jpg", "rover": {"name": "Curiosity"}, "camera": {"full_name": "Mock Cam", "name": "MAST"}},
                     {"id": 2, "img_src": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Curiosity_Self-Portrait_at_%27Big_Sky%27_Drill_Site.jpg", "rover": {"name": "Curiosity"}, "camera": {"full_name": "Mock Cam 2", "name": "FHAZ"}}
                 ]
             }
        elif "EPIC" in endpoint:
            # Return a list of mock EPIC images (needs structure compatible with app)
            # Typically returns a list of dicts
            return [
                {
                    "identifier": "20260101000000",
                    "caption": "Mock Earth Image",
                    "image": "epic_1b_20161011002313", # Dummy filename, won't load from NASA archive but handled by app logic
                    "date": "2016-10-11 00:23:40"
                }
            ]
        elif "neo" in endpoint:
             # Basic NEO mock
             today = datetime.date.today().strftime("%Y-%m-%d")
             return {
                 "near_earth_objects": {
                     today: [
                         {"id": "mock1", "name": "Mock Asteroid", "estimated_diameter": {"kilometers": {"estimated_diameter_max": 0.5, "estimated_diameter_min": 0.4}}, "is_potentially_hazardous_asteroid": True, "close_approach_data": [{"relative_velocity": {"kilometers_per_hour": "20000"}, "miss_distance": {"kilometers": "500000"}, "close_approach_date_full": "2023-Jan-01 12:00"}]}
                     ]
                 }
             }

        return None

    def get_apod(self):
        """Get Astronomy Picture of the Day"""
        return self._get("/planetary/apod")

    def get_neo_feed(self, start_date=None, end_date=None):
        """Get Near Earth Object Feed"""
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = start_date # Default to single day
        
        return self._get("/neo/rest/v1/feed", {"start_date": start_date, "end_date": end_date})

    def get_epic_images(self, date=None):
        """Get EPIC Earth Images"""
        # Default to most recent available date usually involves checking /api/natural, 
        # but for simplicity we'll just get the latest natural images
        if date:
             return self._get(f"/EPIC/api/natural/date/{date}")
        return self._get("/EPIC/api/natural")

    def get_mars_rover_photos(self, sol=1000, rover="curiosity"):
        """Get Mars Rover Photos"""
        return self._get(f"/mars-photos/api/v1/rovers/{rover}/photos", {"sol": sol})

    def search_images(self, query):
        """Search NASA Image and Video Library (Different Base URL)"""
        url = "https://images-api.nasa.gov/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = self.session.get(url, params={"q": query, "media_type": "image"}, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching images: {e}")
            # Mock Search Results
            return {
                "collection": {
                    "items": [
                        {
                            "data": [{"title": "Mock Search Result 1", "description": "Mock description", "nasa_id": "1"}],
                            "links": [{"href": "https://upload.wikimedia.org/wikipedia/commons/e/e1/FullMoon2010.jpg"}]
                        },
                         {
                            "data": [{"title": "Mock Search Result 2", "description": "Mock description", "nasa_id": "2"}],
                            "links": [{"href": "https://upload.wikimedia.org/wikipedia/commons/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg"}]
                        }
                    ]
                }
            }
